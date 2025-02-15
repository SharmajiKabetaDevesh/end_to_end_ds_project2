import os,sys
from src.exception.exception import DSException
from src.constants import training_pipeline
from src.entity.config_entity import TrainingPipelineConfig,Data_Transformation_Config,ModelTrainerConfig
from src.entity.artifact_entity import Data_Transformation_Artifact,ModelTrainerArtifact
from src.utils.utils import save_object,load_object,save_numpy_array_data,load_numpy_array_data,evaluate_models
from src.utils.ml_metrics_utils import get_classification_metrics
from src.entity.artifact_entity import ClassificationMetricArtifact
import numpy as np
import pandas as pd
from src.logging.logger import logging
from sklearn.linear_model import LogisticRegression

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
from sklearn.model_selection import GridSearchCV
from src.utils.model_estimator import NetworkModel

class Model_Trainer:
    def __init__(self,data_transformation_artifact:Data_Transformation_Artifact,model_trainer_config:ModelTrainerConfig):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise DSException(e,sys)
    
    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                "logistic_regression": LogisticRegression(),
                "knn": KNeighborsClassifier(),
                "decision_tree": DecisionTreeClassifier(),
                "ada_boost": AdaBoostClassifier(),
                "gradient_boosting": GradientBoostingClassifier(),
                "random_forest": RandomForestClassifier()
            }
            params = {
                "logistic_regression": {
                    "C": [0.01, 0.1, 1],
                     "solver": ["liblinear", "lbfgs"]
                },
                "knn": {
                    "n_neighbors": [3, 5, 9],
                 },
                "decision_tree": {
                    "max_depth": [None, 10, 20],
                    "min_samples_leaf": [1, 2, 5]
                },
                "ada_boost": {
                    "learning_rate": [0.01, 0.1, 1],
                },
                "gradient_boosting": {
                    "learning_rate": [0.01, 0.1, 0.2],
                    "max_depth": [3, 5, 7],
                },
                "random_forest": {
                    "max_depth": [None, 10, 20, 30],
                }
            }
            model_report: dict = evaluate_models(x_train, y_train, x_test, y_test, models, params)
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]
            logging.info(f"Best Model: {best_model_name} with score: {best_model_score}")
            print(f"Best Model: {best_model_name} with score: {best_model_score}")
            y_train_pred = best_model.predict(x_train)
            classification_train_metric = get_classification_metrics(y_train, y_train_pred)
            y_test_pred=best_model.predict(x_test)
            classification_test_metric=get_classification_metrics(y_test,y_test_pred)
            preprocessor=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=best_model)
            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
     
            )
                # model_report=model_report,
                # best_model_name=best_model_name,
                # best_model_score=best_model_score  
            return model_trainer_artifact
        except Exception as e:
            raise DSException(e, sys)
     
    def initiate_model_trainer(self):
        try:
            train_arr=load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr=load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)
            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            model_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_artifact

        except Exception as e:
            raise DSException(e,sys)   

