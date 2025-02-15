import yaml
from src.exception.exception import DSException
from src.logging.logger import logging
import os,sys
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import pickle
from src.utils.ml_metrics_utils import get_classification_metrics
def read_yaml(file_path)-> dict:
    try:
        with open(file_path,'r')as file:
            return yaml.safe_load(file)
    except Exception as e:
        DSException(e,sys)

def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if(os.path.exists(file_path)):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        DSException(e,sys)


def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise DSException(e,sys)
    

def save_object(file_path:str,obj:object)->None:
    try:
        logging.info("Saving the object given from transformation class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("The object was saved successfully")
    except Exception  as e:
        raise DSException(e,sys)

def load_numpy_array_data(file_path:str)->np.array:
    try:
        logging.info("Loading the numpy array given from tansformed artiafacts")
        if not os.path.exists(file_path):
            raise Exception(f"{file_path} does not exist")       
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)    
    except Exception as e:
        raise DSException(e,sys)
    

def load_object(file_path:str)->object:
    try:
        logging.info("Loading the model/object given from Model artiafacts")
        if not os.path.exists(file_path):
            raise Exception(f"{file_path} does not exist")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"rb") as file_obj:
            pickle.load(file_obj)
        logging.info("The model/object was loaded successfully")
    except Exception  as e:
        raise DSException(e,sys)
    
def evaluate_models(x_train,y_train,x_test,y_test,models,params):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=params[list(models.keys())[i]]
            gs=GridSearchCV(model,param_grid=para,cv=3)
            gs.fit(x_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)
            y_train_pred=model.predict(x_train) 
            y_test_pred=model.predict(x_test)
            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            report[list(models.keys())[i]]=test_model_score
        return report
    except Exception as e:
        raise DSException(e,sys)