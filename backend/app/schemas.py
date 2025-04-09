from pydantic import BaseModel
from typing import Optional


class DecoratedDataSampleSchema(BaseModel):
    search_id: str
    ond: Optional[str]
    advance_purchase: Optional[int]
    request_dep_date: Optional[str]
    request_return_date: Optional[str]
    passengers_string: Optional[str]
    trip_type: Optional[str]
    price_eur: Optional[float]
    main_airline: Optional[str]

    class Config:
        orm_mode = True
