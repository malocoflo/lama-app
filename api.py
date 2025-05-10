import logging
import os
import uvicorn

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from fastapi.security import APIKeyHeader

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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_header = APIKeyHeader(
    name=ACCESS_TOKEN_HEADER_NAME
)

@app.post('/predict',
          response_model=ResponseModel,
          status_code=201)
async def llm(item: Requestmodel,
              token: str = Depends(api_key_header)):
    logger.info('New request is coming!')
    if token != ACCESS_TOKEN:
        return {"error": "InvalidAccessToken"}    
    else:
        predictions = predict(item.question)
        logger.info('Predictions made successfully')
        return ResponseModel(answer=predictions)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)