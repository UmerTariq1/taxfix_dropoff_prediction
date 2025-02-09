# app.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.controllers import prediction_controller
import joblib
import os
from src.services.prediction_service import load_model_and_preprocessor
from src.utils.custom_logger import app_logger as logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global model, preprocessor
    try:
        load_model_and_preprocessor()
        logger.info("Model and preprocessor loaded successfully.")
        print("Model and preprocessor loaded successfully.")
    except FileNotFoundError as e:
        logger.error(f"Error loading model or preprocessor: {e}")
        print(f"Error loading model or preprocessor: {e}")
        raise e
    yield
    # Shutdown
    # Add any cleanup code here if needed

app = FastAPI(lifespan=lifespan)
app.include_router(prediction_controller.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}