from fastapi import FastAPI, Query, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.bdd.database import get_db
from app.bdd.models import DecoratedDataSample
from app.schemas import DecoratedDataSampleSchema


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/test-db", response_model=DecoratedDataSampleSchema)
def test_db(db: Session = Depends(get_db)):
    first_entry = db.query(DecoratedDataSample).first()
    if not first_entry:
        return {"status": "OK", "message": "La table est vide"}
    return first_entry
