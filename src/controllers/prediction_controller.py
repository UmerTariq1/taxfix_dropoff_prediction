# controllers/prediction_controller.py
from fastapi import APIRouter, HTTPException, File, UploadFile
from src.models.request_models import PredictionRequest, RetrainRequest
from src.services.prediction_service import predict_single, retrain_model
from src.utils.custom_logger import app_logger as logger, prediction_logger as pred_logger
import pandas as pd
from pydantic import ValidationError
import time, asyncio
import uuid

router = APIRouter()

@router.post("/predict")
async def predict(data: PredictionRequest):
    request_id = str(uuid.uuid4())
    try:
        start_time = time.time()

        logger.info(f"Received data for prediction: {data}")
        input_data = pd.DataFrame([data.model_dump()])
        
        logger.info("Data received for prediction. Making prediction...")

        prediction, probability = await predict_single(input_data)
        
        logger.info(f"Prediction: {prediction}, Probability: {probability}")

        end_time = time.time()
        logger.info(f"Prediction took: {end_time - start_time} seconds")

        # Log prediction metrics
        await pred_logger.log_prediction({
            "request_id": request_id,
            "input_features": data.model_dump(),
            "prediction": int(prediction),
            "probability": float(probability),
            "processing_time": time.time() - start_time,
            "timestamp": time.time()
        })

        return {"prediction": prediction, "probability": probability}
        
    except Exception as e:
        logger.error(f"Error making prediction for request_id {request_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# From service : async def retrain_model(data_path: pd.DataFrame, val_size=0.2, inference_size=0.05, model_path='output_models/model.pkl', preprocessor_path='output_models/preprocessor.pkl'):

@router.post("/retrain")
def retrain(request: RetrainRequest):
    try:
        start_time = time.time()

        logger.info("Retraining : Retraining model...")
        logger.info(f"Retraining : Data path: {request.data_path}")

        # sleep for 5 seconds using time
        # time.sleep(5)

        retrain_model(request.data_path, request.val_size, request.inference_size, request.model_path, request.preprocessor_path)
        
        logger.info("Retraining : Model retrained successfully.")
        
        end_time = time.time()
        logger.info(f"Retraining : Retraining took: {end_time - start_time} seconds")

        return {"status": "Model retrained successfully."}
        
    except ValidationError as e:
        logger.error(f"Validation error: {e}")

        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error retraining model: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# health check
@router.get("/health")
def health_check():
    return {"status": "ok"}
