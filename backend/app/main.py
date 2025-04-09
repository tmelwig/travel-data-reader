from fastapi import FastAPI, Query, Depends
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from datetime import date
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.bdd.database import get_db
from app.bdd.models import DecoratedDataSample
from app.schemas import DecoratedDataSampleSchema, PriceEvolutionResponse


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

@app.get("/ond")
def get_all_ond(db: Session = Depends(get_db)):
    onds = db.query(DecoratedDataSample.ond).distinct().all()
    ond_list = sorted([ond[0] for ond in onds if ond[0] is not None])
    return {"ond": ond_list}

@app.get("/price-evolution", response_model=List[PriceEvolutionResponse])
def price_evolution(
    ond: str = Query(...),
    trip_type: str = Query(..., regex="^(OW|RT)$"),
    search_country: Optional[str] = None,
    search_date_min: Optional[date] = None,
    search_date_max: Optional[date] = None,
    request_dep_date_min: Optional[date] = None,
    request_dep_date_max: Optional[date] = None,
    stay_duration_min: Optional[int] = None,
    stay_duration_max: Optional[int] = None,
    nb_connections: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(
        DecoratedDataSample.main_airline,
        DecoratedDataSample.advance_purchase,
        func.count().label("recommendation_count"),
        func.percentile_cont(0.5).within_group(DecoratedDataSample.price_eur).label("median_price_eur")
    ).filter(
        DecoratedDataSample.ond == ond,
        DecoratedDataSample.trip_type == trip_type,
        DecoratedDataSample.price_eur.isnot(None)
    )

    if search_country:
        query = query.filter(DecoratedDataSample.search_id.ilike(f"{search_country}-%"))
    if search_date_min:
        query = query.filter(DecoratedDataSample.search_id.contains(str(int(search_date_min.strftime("%s")))))
    if search_date_max:
        query = query.filter(DecoratedDataSample.search_id.contains(str(int(search_date_max.strftime("%s")))))
    if request_dep_date_min:
        query = query.filter(DecoratedDataSample.request_dep_date >= request_dep_date_min)
    if request_dep_date_max:
        query = query.filter(DecoratedDataSample.request_dep_date <= request_dep_date_max)
    if stay_duration_min and stay_duration_max:
        # Calcul de la durée en jours entre les dates de départ et de retour
        query = query.filter(
            (DecoratedDataSample.request_return_date - DecoratedDataSample.request_dep_date).cast(Integer)
            .between(stay_duration_min, stay_duration_max)
        )
    if nb_connections is not None:
        query = query.filter(DecoratedDataSample.search_id.ilike(f"%-{nb_connections}"))  # à adapter si info ailleurs

    query = query.group_by(
        DecoratedDataSample.main_airline,
        DecoratedDataSample.advance_purchase
    ).order_by("main_airline", "advance_purchase")

    results = query.all()
    return results