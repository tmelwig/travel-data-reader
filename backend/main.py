from fastapi import FastAPI
import boto3
import json

app = FastAPI()

s3_client = boto3.client("s3")

BUCKET_NAME = "TODO"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{OnDId}")
async def get_OnD(OnDId: str, oneWay: bool = False):
    try:
        obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=OnDId)
        data = obj["Body"].read().decode("utf-8")
        return json.loads(data)
    except Exception as e:
        return {"error": str(e)}
