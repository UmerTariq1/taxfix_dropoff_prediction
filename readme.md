# Tax Filing Completion Predictor


## Project Overview
This project implements a machine learning solution to predict whether users will complete their tax filing based on their activity patterns, demographics, and platform engagement. The system is built as a production-ready API service with capabilities for real-time predictions and model retraining.

You can test the API endpoints (on any software like Postman) at:
- Prediction: https://tax-prediction-api.onrender.com/predict
- Retraining: https://tax-prediction-api.onrender.com/retrain
- Health Check: https://tax-prediction-api.onrender.com/health

### Features
- Real-time prediction API endpoint (with Asynchronous processing)
- Model retraining capability
- Comprehensive logging system
- CI/CD pipeline with GitHub Actions
- Automated testing suite
- Dockerized application
- Docker image hosted on Docker Hub (accessable at : https://hub.docker.com/r/umertariq01/tax-prediction-api/)
- Docker container hosted on render (accessable at : https://tax-prediction-api.onrender.com/) 

## Technical Stack
- FastAPI for API development
- Scikit-learn for machine learning
- Pandas for data processing
- Docker for containerization
- GitHub Actions for CI/CD
- Pytest for testing

## Project Structure
```
├── src         # contains the code of the application
    ├── controllers/*  # API endpoints
    ├── models/*  # data sctructure of the requests
    ├── services/*  # business logic. functions that are called by the controllers
    ├── utils/*  # utilities like data processing (ingestion), logger, analysis of the data
    ├── train/*  # contains the training logic
├── tests/*  # test cases    
├── data/*  # Dataset files and output models
├── logs/*  # logs of the app
├──--------------------------- 
├── app.py # Main FastAPI application
```

## Installation & Setup

### Setup
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

3b. Run the application on local with docker (docker should be installed):
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
- **Sample Response**:
```json
{
    "status": "ok"
}
```


### Retraining
- **URL**: `http://127.0.0.1:8000/retrain`
- **Method**: POST
- **Sample Request**:
```json
{
  "data_path": "/app/data/dataset.csv"
}
```
- **Sample Response**:
```json
{
    "status": "Model retrained successfully."
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
- **Sample Response**:
```json
{
    "prediction": 1,
    "probability": 1.0
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

### For running the app on local just FastAPI:
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


### Docker Image and Container for Render:
Since this application was developed on m1 machine, the docker architecture by default is arm64. 
But if you want to push the image to docker hub and run it on render, you need to build the image on x86_64 architecture.
```bash
docker build --platform linux/amd64 -t umertariq01/tax-prediction-api:v1 .
docker inspect umertariq01/tax-prediction-api:v1 | grep Architecture
docker tag umertariq01/tax-prediction-api:v1 umertariq01/tax-prediction-api:v1
docker push umertariq01/tax-prediction-api:v1
```
This creates and uploades the docker image on docker hub. 
Now you can use this image to create a container on render.
That container can be accessed at: 

https://tax-prediction-api.onrender.com/