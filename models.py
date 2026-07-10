from sqlalchemy import Column, String, Integer, create_engine,ForeignKey, Table, Float, Date, Table
from sqlalchemy.orm import declarative_base, sessionmaker,relationship
from database import Base


class Gradiliste(Base):
    __tablename__ = 'gradiliste'
    id = Column(Integer, primary_key=True)
    naziv = Column(String)
    lokacija = Column(String)
    investitor = Column(String)
    karneti = relationship('Karnet', back_populates='gradiliste')
    radnici = relationship('Zaposleni', back_populates='gradiliste')
    def __repr__(self):
        return f"Gradiliste(id={self.id}, naziv={self.naziv})"
    
class Karnet(Base):
    __tablename__ = 'karnet'
    id = Column(Integer, primary_key=True)
    datum = Column(Date)
    sati = Column(Integer)
    zaposleni_id = Column(Integer, ForeignKey('zaposleni.id'))
    gradiliste_id = Column(Integer, ForeignKey('gradiliste.id'))
    gradiliste = relationship('Gradiliste', back_populates='karneti')
    zaposleni = relationship('Zaposleni', back_populates='karneti')
    def __repr__(self):
        return f"Karnet(id={self.id}, datum={self.datum}, sati={self.sati})"
    
class Zaposleni(Base):
    __tablename__ = 'zaposleni'
    id = Column(Integer, primary_key=True)
    ime_prezime = Column(String)
    radno_mesto = Column(String)
    satnica = Column(Float)
    gradiliste_id = Column(Integer, ForeignKey('gradiliste.id'))
    karneti = relationship('Karnet', back_populates= 'zaposleni')
    gradiliste = relationship('Gradiliste', back_populates='radnici')
    def __repr__(self):
        return f"Zaposleni(id={self.id}, ime={self.ime_prezime})"