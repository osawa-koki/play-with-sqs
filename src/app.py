import os

from fastapi import FastAPI
from mangum import Mangum
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()


@app.get("/api/ping")
def read_root():
    return {"message": "Hello World"}


@app.get("/api/envs")
def read_envs():
    return {"envs": os.environ}


lambda_handler = Mangum(app)
