import requests

from zendesk import Api
from columns_and_schema import *
from datetime import date
from bigquery_upload import BigQueryUpload
import logging
import os,json



os.chdir("/home/dashboards/cron_scripts")

#home_path = "/home/dashboards/cron_scripts"
home_path = os.getcwd()


logging_path = os.path.join(home_path,"cronpy.log")


logging.basicConfig(filename=logging_path,
                    format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG)


class Shoppify:
    def __init__(self):
        self.host = "https://XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.myshopify.com"
        self.bigquery = BigQueryUpload(dataset_name="shopify",autodetect=True)
        self.temp_store = {}
        self.api = Api(token="token")


    
    def get_data(self,url):
        try:
            result = requests.get(url)
            return result.json()
        except:
            return {}


    
    def get_all_keys(self,dl, keys_list):

        if isinstance(dl, dict):
            keys_list += dl.keys()
            map(lambda x: get_keys(x, keys_list), dl.values())
        elif isinstance(dl, list):
            map(lambda x: get_keys(x, keys_list), dl)

    def get_nested_data(self,table_data,data,name,temp_store):
        if(isinstance(data, dict)):
            for tk,tv in table_data.items():
                # print(data,table_data,end="\nOk\n")
                recv_data = data.get(tk,"Not Found anything")
                if(isinstance(recv_data, dict)):
                    if(len(recv_data)>0):
                        self.get_nested_data(table_data.get(tk,{}), recv_data,(name+"_"+tk), temp_store)
                elif(recv_data!="Not Found anything"):
                    temp_store[name+"_"+tk] = recv_data



    def get_max_id(self,table_name):
        query = self.bigquery.client.query(
            f'''

            SELECT max(id) from XXX.shopify.{table_name}

            '''
        )

        result = query.result()

        for row in result:
            if(row[0] is None):
                return ""
            return row[0]

    
    def get_all_ids(self,table_name):
        query = self.bigquery.client.query(
            f'''
            
            SELECT id from XXXX.shopify.{table_name} ORDER BY id ASC

            '''
        )
        result = query.result()
        return result

    def get_orders(self):
        # self.bigquery.create_table("shopify_line_items")
        # self.bigquery.create_table("shopify_tax_lines")
        run_loop = True
        count = 0
        prev_url = None
        chance = 1
        while run_loop:
            max_id = self.get_max_id("orders")
            url = f"{self.host}/admin/api/2021-07/orders.json?status=any&since_id={max_id}&limit=250"
            # url = f"{self.host}/admin/api/2021-07/orders.json?status=any&since_id={max_id}&limit=250&order=id asc"
            if(prev_url==url):
                run_loop = False
            temp = {}
            all_data = []
            upload_another_table_data = {}
            upload_data = self.get_data(url).get("orders",[])
            if(len(upload_data)<=0):
                run_loop = False
            for items in upload_data:
                for key,value in items.items():
                    if(order_table.get(key,"Not found anything")!="Not found anything"):
                        if(isinstance(value, dict)):
                            temp_var = order_table.get(key,{})
                            self.get_nested_data(temp_var, value, key, temp)
                        elif(not isinstance(value, list)):
                            temp[key] = value
                        elif(isinstance(value, list)):
                            temp_var_an = order_table.get(key,{})
                            if(len(temp_var_an)>0):
                                another_all_data = []
                                for another in value:
                                    another_temp = {}
                                    self.get_nested_data(temp_var_an,another,key,another_temp)
                                    another_temp["order_id"] = items.get("id")
                                    another_all_data.append(another_temp)

                                if(upload_another_table_data.get("shopify_"+key,False)):
                                    if(len(another_all_data)):
                                        upload_another_table_data["shopify_"+key]+=another_all_data
                                else:
                                    if(len(another_all_data)):
                                        upload_another_table_data["shopify_"+key] = another_all_data
                                
                all_data.append(temp)
                temp = {}
                # self.get_max_id("orders")
            if(count==1000):    
                # print(upload_another_table_data)
                if(len(all_data)):
                    res = self.bigquery.uploadToBigQuery(schema_name="orders",dataframe=all_data)
                for table_name,data_val in upload_another_table_data.items():
                    res = self.bigquery.uploadToBigQuery(schema_name=table_name,dataframe=data_val)
                if(res==False):
                    run_loop = False
                print("Data Uploaded\n")
                count  = 0
                upload_another_table_data = {}
                all_data = []

            prev_url = url
                
            count+=1
            
        if(len(all_data)):
            res = self.bigquery.uploadToBigQuery(schema_name="orders",dataframe=all_data)
        
        if(len(upload_another_table_data)):
            for table_name,data_val in upload_another_table_data.items():
                res = self.bigquery.uploadToBigQuery(schema_name=table_name,dataframe=data_val)


    def check_and_preprocess(self,data,table_name):
        for key,value in data.items():
            if(isinstance(data[key], dict)):
                self.find_and_create(data[key], table_name)
            if(key in conv_schema[table_name]):
                exist = self.temp_store.get(key,False)
                if not exist:
                    self.temp_store[key] = data[key]


    def find_and_create(self,got_data,table_name):
        if(isinstance(got_data, list)):    
            for data in got_data:
                self.check_and_preprocess(data,table_name)
        elif(isinstance(got_data, dict)):
            for key,value in got_data.items():
                self.check_and_preprocess(got_data, table_name)
                
    def get_transactions(self):
        # ids = self.get_all_ids("orders")
        all_data = []
        prev_url = None
        run_loop = True
        while run_loop:
            max_id = self.get_max_id("orders")
            print(max_id,end="\n")
            url = f"{self.host}/admin/api/2021-07/orders.json?status=any&since_id={max_id}&limit=250"
            # url = f"{self.host}/admin/api/2021-07/orders.json?status=any&since_id={max_id}&limit=250&order=id asc"
            
            if(prev_url==url):
                run_loop = False
            upload_data = self.get_data(url).get("orders",[])
            if(len(upload_data)<=0):
                run_loop = False    
            all_data = []
            for _id in upload_data: 
                url_new = f"{self.host}/admin/api/2021-07/orders/{_id['id']}/transactions.json"
                transc_data = self.get_data(url_new)
                # print(transc_data,end="\n")
                if(len(transc_data)>0): 
                    for i in self.api.preprocess_data(transc_data,"transactions"):
                        # print(i,end="\n\n")
                        self.find_and_create(i,"transactions")
                        if(len(self.temp_store)):    
                            all_data.append(self.temp_store)
                        self.temp_store = {}
            prev_url = url
                    # print(all_data,end="\n\n")
            self.temp_store = {}
            print(all_data[0])
        self.bigquery.uploadToBigQuery(schema_name="transactions",dataframe=all_data)


    def get_order_risks(self):
        # upload_data = self.get_all_ids("orders")
        run_loop = True
        all_data = []
        prev_url = None
        while run_loop:    
            max_id = self.get_max_id("orders")
            url = f"{self.host}/admin/api/2021-07/orders.json?status=any&since_id={max_id}&limit=250"
            upload_data = self.get_data(url)["orders"]
            if(prev_url==url):
                run_loop = False
            if(len(upload_data)<=0):
                run_loop = False
            # self.bigquery.create_table("order_risks")
            count = 0
            for i in upload_data:
                url_new = f"{self.host}/admin/api/2021-07/orders/{i['id']}/risks.json"
                risk_data = self.get_data(url_new).get("risks",[])
                for data in risk_data:
                    all_data.append(data)
                count+=1
                if(count==2000):
                    print("Uploading Batch")
                    self.bigquery.uploadToBigQuery(schema_name="order_risks",dataframe=all_data)
                    all_data = []
                    count=0
            
            prev_url = url
            
        if(len(all_data)):
            self.bigquery.uploadToBigQuery(schema_name="order_risks",dataframe=all_data)
        print("Done")


    def get_order_refunds(self):
        # upload_data = self.get_all_ids("orders")
        all_data = {
            "order_refunds":[],
            "refund_line_items":[]
        }
        count = 0
        run_loop = True
        prev_url = None
        while run_loop:
            max_id = self.get_max_id("orders")
            add_this = f"&since_id={max_id}"
            # url = f"{self.host}/admin/api/2021-07/orders.json?status=any&limit=250{add_this}"
            url = f"{self.host}/admin/api/2021-07/orders.json?status=any&limit=250{add_this}"
            upload_data = self.get_data(url)["orders"]
            if(len(upload_data)<=0):
                run_loop = False
            if(prev_url==url):
                run_loop = False
            for i in upload_data:
                url_new = f"{self.host}/admin/api/2021-07/orders/{i['id']}/refunds.json"
                refunds_data = self.get_data(url_new).get("refunds",[])
                for dt in refunds_data:
                    first_temp = {}
                    for key,value in dt.items():
                        if(isinstance(value, dict)):
                            gt_tb = order_refund_table.get(key,False)
                            # if(gt_tb):
                            #     self.get_nested_data(gt_tb,value,key,first_temp)
                        elif(isinstance(value, list)):
                            second_search = order_refund_table.get(key,"Not Found")
                            if(second_search!="Not Found"):
                                for nt_dt in value:
                                    second_temp = {}
                                    for k2,v2 in nt_dt.items():
                                        if(isinstance(v2, dict)):
                                            gt_new_tb = second_search.get(k2,{})
                                            if(gt_new_tb):
                                                self.get_nested_data(gt_new_tb, v2, k2, second_temp)
                                        elif not (isinstance(v2, dict) or isinstance(v2, list)):
                                            got_key = second_search.get(k2,"Not Found")
                                            if(got_key!="Not Found"):
                                                second_temp[k2] = v2
                                    if(len(second_temp)):
                                        second_temp["refund_id"] = dt["id"]
                                        all_data["refund_line_items"].append(second_temp)
                        else:
                            fnd_key = order_refund_table.get(key,"Not Found")
                            if(fnd_key!="Not Found"):
                                first_temp[key] = value
                    if(len(first_temp)):
                        all_data["order_refunds"].append(first_temp)
            prev_url = url    
        
        # print(all_data["order_refunds"][0])
        # print(all_data["refund_line_items"][0])
        for k,v in all_data.items():
            if(len(v)):
                self.bigquery.uploadToBigQuery(schema_name=k,dataframe=v)
        
            




    
    def get_all_products(self):
        # self.bigquery.create_table("product")
        # exit()
        run_loop = True
        while run_loop:
            max_id = self.get_max_id("product")    
            url = f"{self.host}/admin/api/2021-07/products.json?limit=250&since_id={max_id}&order=id asc"
            data = self.get_data(url).get("products",[])
            if(len(data)<=0):
                run_loop = False
            all_data = []
            for prdt in data:
                first_temp = {}
                for k,v in  prdt.items():
                    if(isinstance(v, dict)):
                        gt_tb = products_table.get(k,False)
                        if(gt_tb):
                            self.get_nested_data(gt_tb,v,k,first_temp)
                    elif(isinstance(v, list)):
                        gt_tb = products_table.get(k,False)
                    else:
                        gt_tb = products_table.get(k,"Not Found")
                        if(gt_tb!="Not Found"):
                            first_temp[k]=v
                all_data.append(first_temp)

            if(len(all_data)):
                self.bigquery.uploadToBigQuery(schema_name="product",dataframe=all_data)


    def get_product_variant(self):
        # self.bigquery.create_table("product_variants")
        # exit()
        # upload_data = self.get_all_ids("product")
        all_data = []
        run_loop = True
        while run_loop:
            max_id = self.get_max_id("product")    
            url = f"{self.host}/admin/api/2021-07/products.json?limit=250&since_id={max_id}"
            upload_data = self.get_data(url).get("products",[])
            if(len(data)<=0):
                run_loop = False
            for pids in upload_data:
                url = f"{self.host}/admin/api/2021-07/products/{pids['id']}/variants.json?limit=250&order=id asc"
                data = self.get_data(url).get("variants",[])
                for var_dt in data:
                    temp_data = {}
                    for k,v in var_dt.items():
                        table_schema = product_variant_table.get(k,"Not Found")
                        if(table_schema!="Not Found"):
                            temp_data[k] = v
                    all_data.append(temp_data)
            

        if(len(all_data)):
            self.bigquery.uploadToBigQuery(schema_name="product_variants",dataframe=all_data)


    
    def get_payment_disputes(self):
        # self.bigquery.create_table("disputes")
        url = f"{self.host}/admin/api/2021-07/shopify_payments/disputes.json"
        got_data = self.get_data(url).get("disputes")
        all_data = []
        for dt in got_data:
            temp_data={}
            for k,v in dt.items():
                gt_tab = disputed_table.get(k,"Not Found")
                if(gt_tab!="Not Found"):
                    temp_data[k] = v
            all_data.append(temp_data)
        
        if(len(all_data)):
            self.bigquery.uploadToBigQuery(schema_name="disputes",dataframe=all_data)

            

if "__main__" == __name__:    
    shop = Shoppify()
    #shop.get_transactions()
    #shop.get_order_risks()
    shop.get_order_refunds()
    shop.get_orders()
    #shop.get_product_variant()
    #shop.get_all_products()
    #shop.get_payment_disputes()




