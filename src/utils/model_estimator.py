from src.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os,sys
from src.exception.exception import DSException
from src.logging.logger import logging

class NetworkModel:
    def __init__(self,processor,model):
        try:
            self.processor=processor
            self.model=model
        except Exception as e:
            raise DSException(e,sys)
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transform)
            return  y_hat
        except Exception as e:  
            raise DSException(e,sys)