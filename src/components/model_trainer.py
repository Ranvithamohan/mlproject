import os
import sys
from dataclasses import dataclass


from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging



# in utils.py i have saveobject function which i imported here

from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    trainer_model_file_path = os.path.join("artifacts","model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("splitting train and test data")
            X_train, y_train, X_test, y_test = (
                train_array [:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            #create dictionary of all the models
            models = {
                "Random Forest" : RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting" : GradientBoostingRegressor(),
                "Linear Regression" : LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor" : AdaBoostRegressor(),
            }

            params = {
                "Random Forest" : {
                    'n_estimators' : [8,16,32,64,128,256]
                },
                "Decision Tree" : {
                    'criterion' : ['squared_error', 'friedman_mse','absolute_error','poisson']
                },
                "Gradient Boosting" : {
                    'learning_rate' : [.1,.01,.05,.001],
                    'subsample' : [0.6,0.7,0.75,0.8,0.85,0.9],
                    'n_estimators' : [8,16,32,64,128,256]
                },
                 
                "Linear Regression" : {},
                "K-Neighbors Regressor": {
                    'n_neighbors' : [5,7,9,11]
                },
                "XGBRegressor": {
                    'learning_rate' : [.1,.01,.05,.001],
                    'n_estimators' : [8,16,32,64,128,256]
                },
                "CatBoosting Regressor": {
                    'depth' : [6,8,10],
                    'learning_rate' : [.1,.01,.05,.001],
                    'iterations' : [30,50,100]
                },
                "AdaBoost Regressor" :  {
                    'learning_rate' : [.1,.01,.05,.001],
                    'n_estimators' : [8,16,32,64,128,256]
                }


            }

            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,param=params)


            #for getting best model score from dictionary
            best_model_score = max(sorted(model_report.values()))

            #for getting best model name 

            best_model_name = list(model_report.keys()) [
                list(model_report.values()).index(best_model_score)
            ]



            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("no best model found")
            logging.info(f"best model found on training and testing data")

            save_object (
                file_path = self.model_trainer_config.trainer_model_file_path,
                obj= best_model
            )
        
            predicted = best_model.predict(X_test)
            r2_val = r2_score(y_test,predicted) 

            return r2_val
        
        except Exception as e:
            raise CustomException(e,sys)

        