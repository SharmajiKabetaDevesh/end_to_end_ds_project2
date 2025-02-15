import os
import sys
import numpy as np
import pandas as pd


#constant values for data_ingestionworkflow
TARGET_COLUMN="Result"
PIPELINE_NAME="DSPRJ2"
ARTIFACTS_DIR="artifacts"
FILE_NAME="phisingData.csv"    
TRAIN_FILE_NAME="train.csv"
TEST_FILE_NAME="test.csv"



DATA_INGESTION_COLLECTION_NAME="PhisingData"
DATA_INGESTION_DATABASE_NAME="DeveshMlops"
DATA_INGESTION_DIR_NAME="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR="feature_store"
DATA_INGESTION_INGESTED_DIR="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO=0.2


DATA_VALIDATION_DIR_NAME="data_validation"
DATA_VALIDATION_VALID_DIR="validated"
DATA_VALIDATION_INVALID_DIR="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME="report.yaml"


SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

## Data Tranformation COnstants

DATA_TRANSFORMATION_DIR_NAME="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR="transfomed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR="transformed_object"
PREPROCESSING_OBJECT_FILE_NAME="imputerdata.pkl"
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict={
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}


#Model training constants
MODEL_TRAINER_DIR_NAME="model_training_arcs"
MODEL_TRAINER_TRAINED_MODEL_DIR="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NSME="model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float=0.7
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD:float=0.05

SAVED_MODEL_DIR=os.path.join("saved_models")
MODEL_FILE_NAME="model.pkl"