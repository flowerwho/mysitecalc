from sqlalchemy import Column, String, Integer, create_engine,ForeignKey, Table, Float
from sqlalchemy.orm import declarative_base, sessionmaker,relationship


Base = declarative_base()
engine = create_engine("sqlite:///pasosi.db")

class Gradiliste(Base):
    __tablename__ = 'gradiliste'
    id = Column(Integer, primary_key=True)
    naziv = Column(String)
    lokacija = Column(String)
    investitor = Column(String)


class Zaposleni(Base):
    __tablename__ = 'zaposleni'
    id = Column(Integer, primary_key=True)
    ime_prezime = Column(String)
    radno_mest = Column(String)
    satnica = Column(Float)
    gradiliste_id = Column(Integer,ForeignKey('gradiliste.id'))

class Karnet(Base):
    __tablename__ = 'karnet'
    id = Column(Integer, primary_key=True)
    datum = Column(String)
    sati = Column(Integer)
    zaposleni_id = Column(Integer, ForeignKey('zaposleni.id'))
    gradiliste_id = Column(Integer, ForeignKey('gradiliste.id'))
    



Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()



