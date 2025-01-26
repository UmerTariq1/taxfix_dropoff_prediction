# models/user_data.py
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    age: int
    income: float
    employment_type: str
    marital_status: str
    time_spent_on_platform: float
    number_of_sessions: int
    fields_filled_percentage: float
    previous_year_filing: int
    device_type: str
    referral_source: str

class RetrainRequest(BaseModel):
    data_path: str
    val_size: float = 0.2
    inference_size: float = 0.05
    model_path: str = 'output_models/model.pkl'
    preprocessor_path: str = 'output_models/preprocessor.pkl'
