import yaml
from src.exception.exception import DSException
from src.logging.logger import logging
import os,sys
import numpy as np
# import dill
import pickle

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