import os
from dotenv import load_dotenv
import json
import pymongo
import sys
import certifi
ca=certifi.where()
load_dotenv()
from src.exception.exception import DSException
from src.logging.logger import logging

uri=os.getenv("MONGO_URI")

# print(uri)
import pandas as pd
import numpy as np


class DataExtraction():

    def __init__(self):
        try:
            pass
        except Exception as e:
            raise DSException(e,sys)
    
    def cv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=data.to_dict(orient="records")
            return records
        except Exception as e:
            raise DSException(e,sys)
    
    def insert_data_on_mongo(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.mongo_client=pymongo.MongoClient(uri)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
        except Exception as e:
            raise DSException(e,sys)
        
if __name__ =="__main__":
    file_path="Dataep\phisingData.csv"
    database="DeveshMlops"
    collection="PhisingData"
    obj=DataExtraction()
    records=obj.cv_to_json_converter(file_path)
    obj.insert_data_on_mongo(records,database,collection)


    