import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.exception.exception import DSException
from src.logging.logger import logging
from src.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,Data_Transformation_Config,ModelTrainerConfig
from src.entity.artifact_entity import ClassificationMetricArtifact,ModelTrainerArtifact
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import Model_Trainer
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
        print("Data Validation comleted")
        logging.info("Data Transformation began")
        data_transformation_config=Data_Transformation_Config(trainingpipelineconfig=trainingpipelineconfig)
        datatransformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=datatransformation.initiate_transformation()
        logging.info("Data Transformation ended")
        print("Data Transformationn ended")
        logging.info("Model Training began")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        modeltrainer=Model_Trainer(data_transformation_artifact,model_trainer_config)
        model_trainer_artifact=modeltrainer.initiate_model_trainer()
        print(model_trainer_artifact)
        logging.info("Model Training  ended")
        print("Model Training ended")
        
    except Exception as e:
        logging.error(e)
        raise DSException(e,sys)

