import os
import sys
import dill
from src.exception import CustomException

import numpy as np
import pandas as pd

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV



def save_object(file_path, obj) :
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e,sys)
    




def evaluate_models(X_train,y_train,X_test,y_test,models,param) :
    try:
        report = {}
        for i in range(len(list(models))):
            model_name = list(models.keys())[i]  # Get model name
            model = models[model_name]  # Get model object
            para = param.get(model_name, {})
            if para:
                gs = GridSearchCV(model, para, cv=3)
                gs.fit(X_train, y_train)
                best_model = gs.best_estimator_
            else:
                best_model = model

            best_model.fit(X_train, y_train)


           

            # model.fit(X_train,y_train)  #train the model

            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
        
        return report
    
    except Exception as e:
        raise CustomException(e,sys)
    
def load_object(file_path) : #it loads the pickle file 
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)