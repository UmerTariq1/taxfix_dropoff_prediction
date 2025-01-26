import logging
import logging.handlers
import asyncio
from typing import Dict, Any
import aiofiles
import json
from datetime import datetime

class ApplicationLogger:
    _instance = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApplicationLogger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        """Initialize the logger with configuration"""
        logging.basicConfig(
            filename='logs.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self._logger = logging.getLogger(__name__)

    def info(self, message: str):
        self._logger.info(message)

    def error(self, message: str):
        self._logger.error(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def debug(self, message: str):
        self._logger.debug(message)


class AsyncPredictionLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AsyncPredictionLogger, cls).__new__(cls)
            cls._instance.filename = 'prediction_logs.json'
        return cls._instance

    async def log_prediction(self, data: Dict[str, Any]):
        """
        Asynchronously log prediction data in JSON Lines format
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            **data
        }
        
        async with aiofiles.open(self.filename, mode='a') as f:
            await f.write(json.dumps(log_entry) + '\n')


# Singleton instances
app_logger = ApplicationLogger()
prediction_logger = AsyncPredictionLogger()