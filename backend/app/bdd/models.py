from sqlalchemy import Column, Integer, String, Float
from app.bdd.database import Base

class DecoratedDataSample(Base):
    __tablename__ = "decorated_data_sample"
    __table_args__ = {"extend_existing": True}

    search_id = Column(String, primary_key=True)
    ond = Column("OnD", String)
    advance_purchase = Column(Integer)
    request_dep_date = Column(String)
    request_return_date = Column(String)
    passengers_string = Column(String)
    trip_type = Column(String)
    price_eur = Column(Float)
    main_airline = Column(String)
