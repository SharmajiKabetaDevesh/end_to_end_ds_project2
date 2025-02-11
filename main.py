import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.exception.exception import DSException
from src.logging.logger import logging
from src.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig

if __name__=="__main__":
    try:
        logging.info("Data Ingestion Started")
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingestionconfig)
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        logging.info("Data Ingested successfully")
        logging.info("Data Valiation Started")
        
        datavalidation_config=DataValidationConfig(trainingpipelineconfig)
        datavalidation=DataValidation(datavalidation_config,dataingestionartifact)
        data_validation_artifact=datavalidation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data Valiation successfully")
        
    except Exception as e:
        logging.error(e)
        raise DSException(e,sys)

