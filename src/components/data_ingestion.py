# Read data from different sources

import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig, ModelTrainer

@dataclass                                               # To directly define class variable --> If u only want to define variables you can use dataclass
class DataIngestionConfig:
    #Below are the Inputs I will give to DataIngestion Component so that it knows where to save train path , tets path and data path because of this DataIngestionConfig Class
    train_data_path: str =os.path.join("artifacts","train.csv")
    test_data_path: str =os.path.join("artifacts","test.csv")
    raw_data_path: str =os.path.join("artifacts","data.csv")


class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config= DataIngestionConfig()

    def initiate_data_ingestion(self): # If data is stored in db , to read from db this functn will help us
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv("notebook\data\stud.csv")     # Initially for simplicity we will read from csv, Then we will read from mongo DB or API
            logging.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) # If the path exists keep it, if not create a directory in specified path
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info("Train test split initiated")

            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
if __name__=="__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data, test_data)

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))






