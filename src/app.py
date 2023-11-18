import os

import boto3
from dotenv import load_dotenv
from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel

app = FastAPI()
load_dotenv()

client = boto3.client("sqs")

QUEUE_URL = os.environ.get("QUEUE_URL")


class EnqueueModel(BaseModel):
    message_group_id: str
    data: list[str]


class DequeueModel(BaseModel):
    message_group_id: str
    max_number_of_messages: int = 1


@app.get("/api/ping")
def read_root():
    return {"message": "Hello World"}


@app.get("/api/envs")
def read_envs():
    return {"envs": os.environ}


@app.post("/api/enqueue")
def enqueue(model: EnqueueModel):
    for data in model.data:
        client.send_message(
            QueueUrl=QUEUE_URL,
            MessageGroupId=model.message_group_id,
            MessageBody=data,
        )
    return {"message": "Enqueued"}


@app.post("/api/dequeue")
def dequeue(model: DequeueModel):
    result = []
    response = client.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=model.max_number_of_messages,
    )
    messages = response.get("Messages")
    if messages:
        for message in messages:
            result.append(message.get("Body"))
            client.delete_message(
                QueueUrl=QUEUE_URL, ReceiptHandle=message.get("ReceiptHandle")
            )
    return {"message": result}


lambda_handler = Mangum(app)
