import numpy as np
from sklearn.metrics import precision_score,recall_score,f1_score
from src.entity.artifact_entity import ClassificationMetricArtifact
from src.exception.exception import DSException
import sys
def get_classification_metrics(y_true,y_pred):
    try:
        f1=f1_score(y_true,y_pred)
        precision=precision_score(y_true,y_pred)
        recall=recall_score(y_true,y_pred)
        classification_metric=ClassificationMetricArtifact(f1,precision,recall)
        return classification_metric
    except Exception as e:
        raise DSException(e,sys)

