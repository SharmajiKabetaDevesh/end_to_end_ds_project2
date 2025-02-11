from src.exception.exception import DSException
from src.logging.logger import logging
from src.entity.config_entity import DataIngestionConfig
import os
import sys
import pymongo
from sklearn.model_selection import train_test_split
from typing import List
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from src.entity.artifact_entity import DataIngestionArtifact
load_dotenv()

uri=os.getenv("MONGO_URI")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
           self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise DSException(e,sys)
    
    #helps to retrieve data from mongodb
    def export_collections_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(uri)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id"in df.columns:
                df=df.drop(columns=["_id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise DSException(e,sys)
        
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise DSException(e,sys)
        

    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Data was splitted in to two ")
            logging.info("Exited split_data_as_train-test method of data ingestion class")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Exporting the train and test data")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True) 
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)   
            logging.info("splitted Data is saved at location ")
        except Exception as e:
            raise DSException(e,sys)
        

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collections_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(
                self.data_ingestion_config.training_file_path,
                self.data_ingestion_config.testing_file_path
            )
            return dataingestionartifact
        except Exception as e:
            raise DSException(e,sys)
