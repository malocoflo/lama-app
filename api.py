import logging
import os
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI

from api_functions.request import Requestmodel
from api_functions.response import ResponseModel
from api_functions.inference import predict

load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_HEADER_NAME = os.getenv(
    'ACCESS_TOKEN_HEADER_NAME'
)

LOGGING_DIR = os.getenv('LOGGING_DIR')
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL')
LOGGING_FORMAT = os.getenv('LOGGING_FORMAT')

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)

fh = logging.FileHandler(LOGGING_DIR)
fh.setLevel(LOGGING_LEVEL)
formatter = logging.Formatter(
    LOGGING_FORMAT
)

fh.setFormatter(formatter)
logger.addHandler(fh)

app = FastAPI(docs_url=None, redoc_url=None)

@app.post('/predict', status_code=201)
async def llm(item: Requestmodel):
    logger.info('New request is coming!')
    predictions = predict(item.question)
    logger.info('Predictions made successfully')
    return ResponseModel(answer=predictions)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)