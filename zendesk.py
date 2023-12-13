import requests
import os
import logging
import json
from columns_and_schema import *
from datetime import date,datetime,timedelta

from bigquery_upload import BigQueryUpload


os.chdir("/home/dashboards/cron_scripts")



home_path = "/home/dashboards/cron_scripts"
#home_path = os.getcwd()


logging_path = os.path.join(home_path,"cronpy.log")


logging.basicConfig(filename=logging_path,
                    format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG)

class Api:
    def __init__(self, **kwargs):  
        self.current_time = kwargs.get("current_time",date.today().strftime("%s"))
        self.token = kwargs.get("token", False)
        assert self.token, "Please Provide Token"
        self.bigquery = BigQueryUpload()

    def get_headers(self):
        headers = {
            'Authorization': f'Basic {self.token}'
        }

        return headers

   


    def preprocess_data(self, data, key_name):
        new_data = data.get(key_name, False)
        if(new_data==False):
            raise Exception(f"{key_name} Key not found")
        # assert new_data==False, f"{key_name} Key Not Found"
        
        return new_data

    def get_data(self, url):
        header = self.get_headers()
        result = requests.get(url, headers=header)
        return result.json()

    def convert_to_string(self,data):
        if data is not None:
            return (",".join(list(data)))
        else:
            return None


    def clean_data(self,data):
        for val in data:
            for key,value in val.items():
                if(key in conversion_conv):
                    val[key] = self.convert_to_string(value)

        return data

    def iterate_upload(self,url,key_name,table_name):
        while url:
            res = self.get_data(url)
            new_data = self.preprocess_data(res, key_name)
            if(len(new_data)):
                self.bigquery.uploadToBigQuery(schema_name=table_name,dataframe = new_data)
                new_url = res.get("next_page", False)
                print(new_url)
                if(url==new_url):
                    url = False
                else:
                    url = new_url
            else:
                url = False

    def get_incremental_call(self):
        print("Started",end="\n\n")
        url = f"https://zugo.zendesk.com/api/v2/channels/voice/stats/incremental/calls.json?start_time={self.current_time}"
        key_name = "calls"
        table_name = "incremental_calls"
        self.iterate_upload(url,key_name,table_name)
        print("ENded",end="\n\n")


    def get_agent_activity(self):
        url = "https://zugo.zendesk.com/api/v2/channels/voice/stats/agents_activity"
        key_name = "agents_activity"
        table_name = "agents_activity"
        self.iterate_upload(url,key_name,table_name)


    def get_ivr(self):
        url = "https://zugo.zendesk.com/api/v2/channels/voice/ivr"
        key_name = "ivrs"
        table_name = "voice_ivr"
        self.iterate_upload(url,key_name,table_name)

    def get_menu_routes(self):
        url = "https://zugo.zendesk.com/api/v2/channels/voice/ivr/XXXXXXXXXXXXX/menus/XXXXXXXXXXXXXX/routes"
        

if "__main__"==__name__:
    logging.info("Started")
                
    token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    # start_date = "1 Jun, 2021"
    # for i in range(146):
    #     current_time = datetime.strptime(start_date,"%d %b, %Y") + timedelta(i)
    #     print(current_time.strftime("%s"))
    api = Api(token=token)
    api.get_incremental_call()
    api.get_agent_activity()
    api.get_ivr()


    logging.info("End")

    # big = BigQueryUpload()
    # big.create_table("incremental_calls")
    # big.create_table("agents_activity")
    # big.create_table("voice_ivr")