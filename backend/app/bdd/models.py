from sqlalchemy import Column, Integer, String, Float, Date

class DecoratedDataSample(Base):
    __tablename__ = "decorated_data_sample"
    __table_args__ = {"extend_existing": True}

    search_id = Column(String, primary_key=True)
    ond = Column("ond", String)
    advance_purchase = Column(Integer)
    request_dep_date = Column(Date)
    request_return_date = Column(Date)
    passengers_string = Column(String)
    trip_type = Column(String)
    price_eur = Column(Float)
    main_airline = Column(String)
