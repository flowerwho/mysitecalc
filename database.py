from sqlalchemy import Column, String, Integer, create_engine,ForeignKey, Table, Float
from sqlalchemy.orm import declarative_base, sessionmaker,relationship


Base = declarative_base()
engine = create_engine("sqlite:///pasosi.db")

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()