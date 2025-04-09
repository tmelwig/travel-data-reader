from sqlalchemy import Column, Integer

from .database import Base


class DecoratedOnD(Base):
    __tablename__ = "decorated_ond"

    id = Column(Integer, primary_key=True, index=True)
