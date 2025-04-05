from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from .bdd.database import get_db
from .bdd import models

app = FastAPI()

db = next(get_db())


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{OnDId}")
async def get_OnD(OnDId: str, oneWay: bool = False):
    try:
        return list(map(jsonable_encoder, db.query(models.DecoratedOnD).all()))
    except Exception as e:
        return {"error": str(e)}
