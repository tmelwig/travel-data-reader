from pydantic import BaseModel
from datetime import date

class DecoratedDataSampleSchema(BaseModel):
    search_id: str
    ond: str
    advance_purchase: int
    request_dep_date: date
    request_return_date: date | None = None
    passengers_string: str
    trip_type: str
    price_eur: float
    main_airline: str

    class Config:
        from_attributes = True

class PriceEvolutionResponse(BaseModel):
    main_airline: str
    advance_purchase: int
    median_price_eur: float
    recommendation_count: int