from src.entity.config_entity import DataValidationConfig,TrainingPipelineConfig
from src.exception.exception import DSException
from src.logging.logger import logging
from src.entity.artifact_entity import DataValidationArtifact
from src.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
from src.utils.utils import read_yaml,write_yaml_file
from src.entity.artifact_entity import DataIngestionArtifact    
import pandas as pd
import numpy as np
import os,sys
class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.schema_config=read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise DSException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise DSException(e,sys)
        
    def validate_number_of_columns(self,data:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self.schema_config)
            logging.info(f"NUmber of columns are{number_of_columns}")
            logging.info(f"NUmber of columns are{data.columns}")
            if len(data)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise DSException(e,sys)
    
    def detect_data_drift(self,base_df,current_df,threshold=0.05)->bool:

        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_sample_dist=ks_2samp(d1,d2)
                is_found:bool=False
                if threshold<=is_sample_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_sample_dist.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)   
        except Exception as e:  
            raise DSException(e,sys)
     
    
    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            train_data=DataValidation.read_data(train_file_path)
            test_data=DataValidation.read_data(test_file_path)
            status=self.validate_number_of_columns(train_data)
            if not status:
                error_message=f"Number of columns in train data is not equal to schema"
            status=self.validate_number_of_columns(test_data)
            if not status:
                error_message=f"Number of columns in test data is not equal to schema"
            #checking data drift
            status=self.detect_data_drift(train_data,test_data)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_data.to_csv(self.data_validation_config.valid_train_file_path,index=False)    
            test_data.to_csv(self.data_validation_config.valid_test_file_path,index=False)  
            datavalidationartifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return datavalidationartifact

        except Exception as e:
            raise DSException(e,sys)    