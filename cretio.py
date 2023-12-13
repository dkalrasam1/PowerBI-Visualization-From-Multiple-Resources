import requests

from zendesk import Api
from bigquery_upload import BigQueryUpload
import json
import pandas as pd
import io
import numpy as np
import os
from datetime import date,timedelta,datetime

os.chdir("/home/dashboards/cron_scripts")


class Cretio:
    def __init__(self,**kwargs):
        self.bigquery = BigQueryUpload(dataset_name="cretio")
        self.client_id = kwargs.get("client_id")
        self.client_secret = kwargs.get("client_secret")
        self.host = "https://api.criteo.com"
        self.token = self.get_token()
        self.current_date = kwargs.get("current_date",(date.today()-timedelta(1)).strftime("%Y-%m-%d"))


    def post_request(self,url,data,headers=False):
        if headers is False:
            headers = {"Content-Type":"application/*+json","Authorization":f"Bearer {self.token}"}
        result = requests.post(url,data=data,headers=headers)
        return result


    def get_token(self):
        url = f"{self.host}/oauth2/token"
        payload = {
            "client_id":self.client_id,
            "client_secret":self.client_secret,
            "grant_type":"client_credentials"
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }

        result = self.post_request(url,payload,headers).json()
        token = result.get("access_token",False)
        assert token,"Token Not Found"
        return token
    
    def get_statistics_data(self):
        url = f"{self.host}/2021-07/statistics/report"
        data = {
    "dimensions":["AdvertiserId", "AdsetId", "CategoryId", 
    "Advertiser", "Adset", "Category", "Device","OS","Hour", "Day", 
    "Week", "Month", "Year"],
    "metrics":["RevenueGeneratedAllClientAttribution",
    "RevenueGeneratedPc30d","RoasClientAttribution","RoasAllClientAttribution","Displays",
    "Clicks","SalesAllClientAttribution","SalesClientAttribution",
    "SalesPc30d","AdvertiserCost","ConversionRateClientAttribution","CostPerOrderClientAttribution"],
    "currency":"EUR",
    "format":"CSV",
    "startDate":f"{self.current_date}T00:00:00.0000000+00:00",
    "endDate":f"{self.current_date}T23:59:00.0000000+00:00"
        }


        result = self.post_request(url,json.dumps(data))
        df = pd.read_csv(io.StringIO(result.text), sep=";",encoding="utf-8-sig")
        df.rename(columns={"ï»¿AdvertiserId":"AdvertiserId"},inplace=True)
        df.replace(np.nan,0,inplace=True)
        df.columns = [i.lower() for i in df.columns]
        df["conversionrateclientattribution"] = df["conversionrateclientattribution"].astype("float")
        df["hour"] = pd.to_datetime(df["hour"]).dt.strftime('%Y-%m-%d %H:%M')
        new_data = df.to_dict("records")
        res = self.bigquery.uploadToBigQuery(schema_name="stastics",dataframe=new_data)
        if res:
            print("Uploaded_on")
        else:
            print("Wrong something")
        
url = "https://api.criteo.com/oauth2/token"

client_id = "XXXXXXXXXXXXXXXXXXXXXx"
client_secret = "XXXXXXXXXXXXXXXXXXXX"
# start_date = "2021-10-29"
# for i in range(2):
#     current_time = datetime.strptime(start_date,"%Y-%m-%d") + timedelta(i)
#     print(current_time.strftime("%Y-%m-%d"))
cr = Cretio(client_id=client_id,client_secret=client_secret)
cr.get_statistics_data()



# payload='client_id=d68d7343886c4433bb4ba70c1405cfc5&client_secret=%2BDunT9n7GtaRhhtY%2BpQuBNEdk7J8pW%2BbiIz%2FCmE8vyZN&grant_type=client_credentials'
# headers = {
#   'Content-Type': 'application/x-www-form-urlencoded'
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)