## Commands

### For running tests:
> .venv/bin/pytest -v

### For running the app on local:
> uvicorn app:app --host 0.0.0.0 --port 8000


### For running the app on docker:
> docker build -t tax-prediction-api .
> docker run -d -p 8000:8000 --name test-container tax-prediction-api

### For running the tests on docker:
> docker run --rm tax-prediction-api pytest -v

### For stopping the app on docker:
> docker stop test-container
> docker rm test-container

### For checking the logs:
> docker logs test-container

### For checking the custom logger logs
> docker exec -it test-container bash
> cat /app/prediction_logs.json
> cat /app/logs.log
