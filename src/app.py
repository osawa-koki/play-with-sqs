from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/api/ping")
def read_root():
    return {"message": "Hello World"}


lambda_handler = Mangum(app)
