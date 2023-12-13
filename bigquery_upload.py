import os
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import date
from columns_and_schema import *
import logging


#os.chdir("/home/dashboards/cron_scripts")
os.chdir("/var/www/html/zugo_bikes")


#home_path = "/home/dashboards/cron_scripts"
home_path = os.getcwd()

logging_path = os.path.join(home_path,"cronpy.log")


logging.basicConfig(filename=logging_path,
                    format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    home_path, "client_secret.json")


class BigQueryUpload:
    def __init__(self, **kwargs):
        self.client = bigquery.Client(
            project=kwargs.get("project_name", "zugo-bike"))
        self.dataset = self.client.dataset(
            kwargs.get("dataset_name", "zugo_report"))
        self.autodetect = kwargs.get("autodetect",False)

    def get_config(self, schema_data=None):
        if(not self.autodetect):    
            job_config = bigquery.LoadJobConfig(schema=schema_data)
            job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
            job_config.autodetect = False
        else:
            job_config = bigquery.LoadJobConfig()
            job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
            job_config.autodetect = True
        return job_config

    def get_table(self, table_name):
        return self.dataset.table(table_name)

    def get_table_new(self,table_name):
        return self.client.get_table(table_name)


    def get_table_schema(self,table_name=False):

        if table_name:
            table = self.get_table_new(self.get_table(table_name))
            print(table.schema,end="\n\n")
        else:    
            tables = [
                "agents_activity",
                "incremental_calls",
                "menu_routes",
                "menus",
                "voice_ivr",
            ]

            for i in tables:
                print(f"{i} table schema\n")
                table = self.get_table_new(self.get_table(i))
                print(table.schema)
                print("\n")

    def create_table(self,table_name):
        table = bigquery.Table(self.get_table(table_name), schema=schema.get(table_name, False))
        res = self.client.create_table(table)
        print(res)


    def check_dataframetype(self, data):
        if(str(type(data)) == "<class 'dict'>"):
            return [data]

        elif(str(type(data)) == "<class 'list'>"):
            return data
        else:
            raise "Not a valid format"

    def add_uploaded_on_data(self,data):
        data["uploaded_on"] = date.today().strftime("%Y-%m-%d")
        return data

    def uploadToBigQuery(self, **kwargs):
        schema_name = kwargs.get("schema_name")
        schema_data = schema.get(schema_name, False)
        assert schema_data, f"{schema_name} does not exist"
        job_config = self.get_config(schema_data)
        # print(job_config)
        # exit()

        upload_data = self.check_dataframetype(kwargs.get("dataframe"))
        table = self.get_table(schema_name)


        upload_data = list(map(self.add_uploaded_on_data,upload_data))

       
        try:
            res = self.client.load_table_from_json(
                upload_data, table, job_config=job_config)
            if(res.result()):
                logging.info("File Uploaded")
                return True
            print("Bigquery errro")
            print(res.errors())
            return False

        except Exception as e:
            print("error printed 2")
            print(str(e))
            return False

