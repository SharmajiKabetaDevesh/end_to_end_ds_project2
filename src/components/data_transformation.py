from src.entity.config_entity import Data_Transformation_Config
from src.exception.exception import DSException
from src.logging.logger import logging
from src.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from src.entity.artifact_entity import Data_Transformation_Artifact,DataValidationArtifact
import numpy as np
import pandas as pd
import sys,os
from src.utils.utils import save_numpy_array_data,save_object
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from src.constants.training_pipeline import TARGET_COLUMN


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
    data_transformation_config:Data_Transformation_Config):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config

        except Exception as e:
            raise DSException(e,sys)
    
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise DSException(e,sys)
    
    def get_data_transformation_object(self)->Pipeline:
        logging.info("Entered get_data_transformed_object of Data Transformation class")
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Intialized the imputer with params")
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise DSException(e,sys)



    def initiate_transformation(self)->Data_Transformation_Artifact:
        logging.info("Initiated the transformation process")
        try:
            logging.info("Started the transformation process")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_features_train_df=train_df[TARGET_COLUMN]
            target_features_train_df=target_features_train_df.replace(-1,0)
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_features_test_df=test_df[TARGET_COLUMN]
            target_features_test_df=target_features_test_df.replace(-1,0)
            preprocessor=self.get_data_transformation_object()
            preprocessor_object=preprocessor.fit(input_feature_train_df) 
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)
            train_arr=np.c_[transformed_input_train_feature,np.array(target_features_train_df)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_features_test_df)]
            save_numpy_array_data(self.data_transformation_config.transformation_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)
            artifacts=Data_Transformation_Artifact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
            transformed_train_file_path=  self.data_transformation_config.transformation_train_file_path,
            transformed_test_file_path=self.data_transformation_config.transformed_test_file_path

            )

            logging.info("The transformation process is ended")
            return artifacts
        except Exception as e:
            raise DSException(e,sys)
