# Tax Filing Completion Predictor


## Project Overview
This project implements a machine learning solution to predict whether users will complete their tax filing based on their activity patterns, demographics, and platform engagement. The system is built as a production-ready API service with capabilities for real-time predictions and model retraining.

### Features
- Real-time prediction API endpoint
- Model retraining capability
- Comprehensive logging system
- Docker support
- CI/CD pipeline with GitHub Actions
- Automated testing suite

## Technical Stack
- FastAPI for API development
- Scikit-learn for machine learning
- Pandas for data processing
- Docker for containerization
- GitHub Actions for CI/CD
- Pytest for testing

## Project Structure
├── controllers/*  # API endpoints
├── data/*  # Dataset files. 
├── logs/*  # logs of the app
├── models/*  # data sctructure of the requests
├── output_models/*  # trained models and preprocessors
├── services/*  # business logic. functions that are called by the controllers
├── utils/*  # utilities like logger and analysis of the data
├──--------------------------- 
├── app.py # Main FastAPI application
├── ingestion.py # Data ingestion/input and preprocessing
├── test_case.py # Test cases for the API
├── train.py # Model training script


## Installation & Setup

### Local Setup
1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

3a. Run the application on local without docker:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

3b. Run the application on local with docker:
```bash
docker build -t tax-prediction-api .
docker run -d -p 8000:8000 --name test-container tax-prediction-api
```

4. Do the health check:
```bash
curl http://localhost:8000/health
```
or send a GET request to http://localhost:8000/health from postman


5. Run the tests:
```bash
.venv/bin/pytest -v
```


## API Endpoints

### Health Check
- **URL**: `http://127.0.0.1:8000/health`
- **Method**: GET


### Retraining
- **URL**: `http://127.0.0.1:8000/retrain`
- **Method**: POST
- **Sample Request**:
```json
{
  "data_path": "/app/data/dataset.csv"
}
```

### Prediction
- **URL**: `http://127.0.0.1:8000/predict`
- **Method**: POST
- **Sample Request**:
```json
{
    "age": 12,
    "income": 75000.5,
    "employment_type": "full_time",
    "marital_status": "married",
    "time_spent_on_platform": 210.5,
    "number_of_sessions": 22,
    "fields_filled_percentage": 95.2,
    "previous_year_filing": 0,
    "device_type": "desktop",
    "referral_source": "organic_search"
}
```


## Testing

### Running the tests on local:
```bash
.venv/bin/pytest -v
```

### Running the tests on docker (make sure the docker container is running):
```bash
docker run --rm tax-prediction-api pytest -v
```


## CI/CD pipeline
The project includes a GitHub Actions workflow that:
- Builds the Docker image
- Runs tests
- Performs health checks
- Tests the prediction and retrain endpoints







----------------------------------------------------------------
## Commands

### For running tests:
```bash
.venv/bin/pytest -v
```

### For running the app on local:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### For running the app on docker:
```bash
docker build -t tax-prediction-api .
docker run -d -p 8000:8000 --name test-container tax-prediction-api
```
### For running the tests on docker:
```bash
docker run --rm tax-prediction-api pytest -v
```

### For stopping the app on docker:
```bash
docker stop test-container
docker rm test-container
```

### For checking the logs:
```bash
docker logs test-container
```

### For checking the custom logger logs (can also be checked in the docker application)
```bash
docker exec -it test-container bash
cat /app/prediction_logs.json
cat /app/logs.log
```
