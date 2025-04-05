from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(".env")

user = "postgres"
password = getenv("POSTGRES_PASSWORD")
server = "database-decorated.c7k8uyae6cbf.eu-north-1.rds.amazonaws.com"
port = "5432"
db_name = "flight_data_decorated"
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{server}:{port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
