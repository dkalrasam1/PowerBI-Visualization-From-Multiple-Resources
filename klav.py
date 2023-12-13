import klaviyo
from requests.api import get
from google.cloud import bigquery
from bigquery_upload import BigQueryUpload
from columns_and_schema import metrics_table,metrics_timeline_table
from datetime import date,datetime
import google.auth
from google.oauth2 import service_account
import json,os
import requests

#os.chdir("/home/dashboards/cron_scripts")
os.chdir("/var/www/html/zugo_bikes")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/var/www/html/zugo_bikes/client_secret.json"

class KlaviyoApi:
    def __init__(self,**kwargs):
        self.private_token = kwargs.get("private_token",False)
        self.public_token = kwargs.get("public_token",False)
        assert (self.private_token and self.public_token),"Please Provide Public and Private token"
        self.client = klaviyo.Klaviyo(public_token=self.public_token, private_token=self.private_token)
        self.bigquery = BigQueryUpload(dataset_name="klaviyo")


    
    def excuteQuery(self,query):
        db_obj = self.bigquery.client.query(query)
        result = db_obj.result()
        for res in result:
            return res[0]


    
    def callBeforeInsert(self,table_name):
        max_id = self.excuteQuery(
            f'''
        SELECT max(page_no) from zugo-bike.klaviyo.{table_name}
        ''')

        query = self.bigquery.client.query(f''' 
        DELETE zugo-bike.klaviyo.{table_name} WHERE page_no={max_id}
        ''')

        result = query.result()

        return max_id


    def get_all_ids(self,table_name):
        query = self.bigquery.client.query(
            f'''
            
            SELECT id from zugo-bike.klaviyo.{table_name} ORDER BY id ASC

            '''
        )

        result = query.result()
        return result


    def get_campaigns(self):
        self.bigquery.create_table("campaigns")
        run_loop = True
        offset = 0
        data = {"campaigns":[],
        "camp_lists":[],
        "camp_excluded_lists":[]}
        while run_loop:
            result = self.client.Campaigns.get_campaigns(count=5000,page=offset)
            for item in result.data["data"]:
                temp = {} 
                for k,v in item.items():    
                    if(isinstance(v, list)):
                        for sb in v:
                            sb["camp_id"] = item["id"]
                            data[f"camp_{k}"].append(sb)
                    else:
                        temp[k] = v
                temp["page_no"] = offset
                data["campaigns"].append(temp)

            if(len(result.data["data"])<=0):
                run_loop = False
            offset+=1
        for k,v in data.items():
            self.bigquery.uploadToBigQuery(schema_name = k,dataframe=v)

    
    def get_campaign_recipients(self):
        self.bigquery.create_table("camp_reciept")
        # exit()
        run_loop = True
        all_data = []
        first_offset = 0
        while run_loop:
            all_campaigns = self.client.Campaigns.get_campaigns(count=5000,page=first_offset)
            for ids in all_campaigns.data["data"]:
                second_loop = True
                second_offset = ""
                while second_loop:
                    try:
                        get_reciept = self.client.Campaigns.get_campaign_recipients(ids["id"],offset=second_offset,count=5000,sort="asc")
                        for dt in get_reciept.data["data"]:
                            dt["camp_id"] = ids["id"]
                            dt["page_no"] = second_offset
                            all_data.append(dt)

                        second_loop = get_reciept.data.get("next_offset",False)
                        second_offset = get_reciept.data.get("next_offset","")
        
                    except Exception as e:
                        print(str(e))
                        second_loop = False
                        second_offset = 0

            first_offset+=1    
            if(len(all_campaigns.data["data"])<=0):
                run_loop = False


        
        if(len(all_data)):
            self.bigquery.uploadToBigQuery(schema_name="camp_reciept",dataframe=all_data)


    def get_nested_data(self,table_data,data,name,temp_store):
        if(isinstance(data, dict)):
            for tk,tv in table_data.items():
                # print(data,table_data,end="\nOk\n")
                recv_data = data.get(tk,"Not Found anything")
                if(isinstance(recv_data, dict)):
                    if(len(recv_data)>0):
                        self.get_nested_data(table_data.get(tk,{}), recv_data,(name+"_"+tk), temp_store)
                elif(recv_data!="Not Found anything"):
                    key = name+"_"+tk
                    if("$"in key):
                        key = key.replace("$", "")
                    if(isinstance(recv_data, list)):
                        temp_store[key] = json.dumps(recv_data)
                    else:
                        temp_store[key] = recv_data




    def get_metrics(self):
        self.bigquery.create_table("metrics")
        # exit()
        run_loop = True
        page = 0
        all_data = []
        while run_loop:    
            result = self.client.Metrics.get_metrics(count=500,page=page)
            for data in result.data["data"]:
                temp_data = {}
                for key,value in data.items():
                    if(isinstance(value, dict)):
                        get_tb = metrics_table.get(key,{})
                        self.get_nested_data(get_tb, value, key, temp_data)
                    elif(not isinstance(value, list)):
                        temp_data[key] = value
                temp_data["page_no"] = page
                all_data.append(temp_data)
            if(len(result.data["data"])<=0):
                run_loop = False
            page+=1
        
        if(len(all_data)):
            self.bigquery.uploadToBigQuery(schema_name="metrics",dataframe=all_data)


    # def get_metrics_timeline(self):
    #     result = self.client.Metrics.get_metric_timeline_by_id(metric_id="McA2zW")
    #     print(result.data["data"][4])


    def preprocess_data_custom(self,data):
        for i in range(len(data)):
            try:
                data[i]["event_properties_event_id"] = str(data[i]["event_properties_event_id"])+" "
            except:
                data[i]["event_properties_event_id"] = None

        return data



    
    def get_metrics_timeline(self):
        self.bigquery.create_table("metrics_timelines")
        # exit()
        all_data = []
        count = 0
        ids_data = self.get_all_ids("metrics")
        for ids in ids_data:
            print(ids[0])
            run_loop = True
            next_token = None
            while run_loop:
                result = self.client.Metrics.get_metric_timeline_by_id(metric_id=ids[0],since=next_token)
                for data in result.data["data"]:
                    temp_data = {}
                    for key,val in data.items():
                        if(isinstance(val, dict)):
                            get_tb = metrics_timeline_table.get(key,{})
                            if(get_tb=="Json_Save"):
                                if("$" in key):
                                    key = key.replace("$","")
                                temp_data[key] = json.dumps(val)
                            elif(isinstance(get_tb, dict)):
                                self.get_nested_data(get_tb, val, key, temp_data)
                        elif(isinstance(val, list)):
                            get_tb = metrics_timeline_table.get(key,False)
                            if(get_tb=="Json_Save"):
                                if("$" in key):
                                    key = key.replace("$","")
                                temp_data[key] = json.dumps(val)
                        elif not (isinstance(val, dict) or isinstance(val, list)):
                            if("$" in key):
                                key = key.replace("$","")
                            temp_data[key] = val 
                    if(len(temp_data)):
                        temp_data["object_type"]=result.data.get("object")
                        temp_data["metric_id"] = ids[0]
                        all_data.append(temp_data)
                    
                    if(len(all_data)==90000):
                        self.bigquery.uploadToBigQuery(schema_name="metrics_timelines",dataframe=self.preprocess_data_custom(all_data))
                        all_data = []
                        print("Batch Upload Done!!!")

                        # print(all_data,end="\n\n")        
                        # break               
                run_loop = result.data.get("next",False)
                next_token = result.data.get("next",False)
        if(len(all_data)):
            self.bigquery.uploadToBigQuery(schema_name="metrics_timelines",dataframe=self.preprocess_data_custom(all_data))

    
    def get_lists(self):
        result = self.client.Lists.get_lists().data
        if(result):
            self.bigquery.uploadToBigQuery(schema_name="lists",dataframe=result)

    
    def get_Request(self,url):
        url = url+f"&api_key={self.private_token}"
        #print(url)
        result = requests.get(url).json()
        return result

    def get_people_exclusion(self):
        self.bigquery.create_table("people_exclusions")
        run_loop = True
        count = 0
        all_data = []
        while run_loop:
            url = f"https://a.klaviyo.com/api/v1/people/exclusions?sort=asc&count=500&page={count}"
            get_data = self.get_Request(url)
            all_data+=get_data.get("data",[])
            run_loop = get_data.get("data",False)
            count+=1
        if(len(all_data)):
            self.bigquery.uploadToBigQuery(schema_name="people_exclusions",dataframe=all_data)
        
    def query_event_data(self,**kwargs):
        #print('----------------------')
        #self.bigquery.create_table("people_exclusions")
        
        count = 1
        all_data = []
        resultsData = []
        #result = self.client.Metrics.get_metrics(count=500)
        url_flow = f'https://a.klaviyo.com/api/v1/flows?'
        get_flow_data = self.get_Request(url_flow)
        
        #print(get_flow_data['data'])
        #exit()
        for data in get_flow_data["data"]:
            # print(data)
            # exit()
            run_loop = True
            if(data['trigger']['type'] == 'Metric'):
                while run_loop:
                    metric_id = data['trigger']['metric']['id']
                    flow_id = data['id']
                    url = f"https://a.klaviyo.com/api/v1/metric/{metric_id}/export?sort=asc&count=500&page={count}&measurement=value&unit=day&by=$attributed_flow"
                    get_data = self.get_Request(url)
                    #raw_data = json.dumps(get_data)
                    #print(raw_data)
                    newData = {}
                    newData['flow'] = flow_id
                    newData['flow_name'] = data['name']
                    
                    for i in get_data : 
                        
                        #print(i)
                        if(type(get_data[i]) is dict or type(get_data[i]) is list and len(get_data[i]) > 0):
                            for k in get_data[i]:
                                if(type(get_data[i]) is list):
                                    #print('t')#for result
                                    for p in get_data[i]:
                                        #print(p)
                                        for j in p['data']:
                                            res = {}
                                            res['segment'] = p['segment']
                                            res['metric'] = get_data['metric']['id']
                                            res['flow'] = data['id']
                                            res['date'] = j['date']
                                            res['values'] = j['values']

                                            resultsData.append(res)
                                else:
                                    if(k == 'integration'):
                                        newData['integration_object'] = get_data[i][k]['object']
                                        newData['integration_category'] = get_data[i][k]['category']
                                        newData['integration_id'] = get_data[i][k]['id']
                                        newData['integration_name'] = get_data[i][k]['name']
                                    else:
                                        newData[k] = get_data[i][k]
                        else:
                            newData[i] = get_data[i]

                    all_data.append(newData)    
                    #print(resultsData)
                    #exit()
                    run_loop = False
                    #print('////////////////////////////////////')
                    count+=1
        #print(all_data)
        
        #print(resultsData)
        #exit()
        if(len(all_data)):
            TableNameFlowMetrics = 'flow_metrics'
            TableNameSegment = 'flow_metrics_segment'
            credentials, project = google.auth.default(
                scopes=[
                    "https://www.googleapis.com/auth/drive",
                    "https://www.googleapis.com/auth/bigquery",
                ]
            )
            self.client = bigquery.Client(credentials=credentials, project='zugo-bike')
            self.dataset = self.client.dataset(kwargs.get("dataset_name", "klaviyo"))
            
            flow_metrics_schema = self.client.get_table('zugo-bike.klaviyo.'+TableNameFlowMetrics).schema
            job_config = bigquery.LoadJobConfig(
                schema=flow_metrics_schema,
                write_disposition=bigquery.job.WriteDisposition.WRITE_TRUNCATE
            )
            flow_metrics = self.client.load_table_from_json(all_data, self.dataset.table(TableNameFlowMetrics), job_config=job_config)

            flow_metrics_segment_schema = self.client.get_table('zugo-bike.klaviyo.'+TableNameSegment).schema
            job_config = bigquery.LoadJobConfig(
                schema=flow_metrics_segment_schema,
                write_disposition=bigquery.job.WriteDisposition.WRITE_TRUNCATE
            )
            flow_metrics_segment = self.client.load_table_from_json(resultsData, self.dataset.table(TableNameSegment), job_config=job_config)
            #print(res)
            print('done')



PUBLIC_TOKEN = "XXXX"

PRIVATE_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"

        


klip = KlaviyoApi(private_token=PRIVATE_TOKEN,public_token=PUBLIC_TOKEN)
# klip.get_campaigns()
# klip.get_campaign_recipients()
# klip.get_metrics()
# klip.get_metrics_timeline()
# klip.get_lists()
# klip.get_people_exclusion()
klip.query_event_data()