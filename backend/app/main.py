from fastapi import FastAPI, Query, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.bdd.database import get_db
from app.bdd.models import DecoratedOnD

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/analytics")
def analytics(
    ond: str = Query(...),
    trip_type: str = Query("OW"),
    dep_date: str = Query(...),
    return_date: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(
        DecoratedOnD.main_airline,
        DecoratedOnD.advance_purchase,
        func.count().label("recommendation_count"),
        func.percentile_cont(0.5).within_group(DecoratedOnD.price_eur).label("median_price_eur")
    ).filter(
        DecoratedOnD.OnD == ond,
        DecoratedOnD.request_dep_date == dep_date,
        DecoratedOnD.trip_type == trip_type,
        DecoratedOnD.price_eur != None
    )

    if return_date:
        query = query.filter(DecoratedOnD.request_return_date == return_date)
    else:
        query = query.filter(DecoratedOnD.request_return_date == None)

    query = query.group_by(
        DecoratedOnD.main_airline,
        DecoratedOnD.advance_purchase
    ).order_by("median_price_eur")

    return [dict(row._mapping) for row in query.all()]
