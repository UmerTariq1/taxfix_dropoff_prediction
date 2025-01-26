# services/prediction_service.py
import joblib
import pandas as pd
from src.utils.ingestion import DataIngestion
import os, asyncio
from src.train.train import train_model, save_model
from src.utils.custom_logger import app_logger as logger

model, preprocessor = None, None


def load_model_and_preprocessor(model_path: str = 'data/output_models/model.pkl', preprocessor_path: str = 'data/output_models/preprocessor.pkl'):
    """Loads the trained model and preprocessor."""

    if not os.path.exists(model_path) or not os.path.exists(preprocessor_path):
        raise FileNotFoundError("Model or preprocessor not found. Please train the model first.")

    global model, preprocessor
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    # return model, preprocessor

    
async def predict_single(data: pd.DataFrame):
    """Makes a prediction for a single user."""

    global model, preprocessor
    
    data_ingestion = DataIngestion()
    processed_data = await data_ingestion.preprocess_test(data, preprocessor=preprocessor)

    
    # sleep for 5 seconds for debugging
    # await asyncio.sleep(5)

    prediction = model.predict(processed_data)
    probability = model.predict_proba(processed_data)[:, 1]


    return int(prediction[0]), float(probability[0])

def retrain_model(data_path: pd.DataFrame, val_size, inference_size, model_path, preprocessor_path):
    """Retrains the model with new data."""
    
    data_ingestion = DataIngestion(file_path=data_path)

    logger.info("Retraining : Data ingestion class initialized")

    data_ingestion.read_data()

    logger.info("Retraining : Data read successfully")

    x_train, x_test, x_inference, y_train, y_test, y_inference, preprocessor, val_size_number, inference_size_number = data_ingestion.preprocess_train(val_size=val_size, inference_size=inference_size)

    logger.info("Retraining : Data preprocessed successfully")

    model, report_ = train_model(x_train, y_train, x_test, y_test)

    logger.info("Retraining : Model trained successfully")
                
    save_model(model, preprocessor, model_path, preprocessor_path)

    logger.info("Retraining : Model saved successfully")

    return report_