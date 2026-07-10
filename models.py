from sqlalchemy import Column, String, Integer,ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Gradiliste(Base):
    __tablename__ = 'gradiliste'
    id = Column(Integer, primary_key=True)
    naziv = Column(String)
    lokacija = Column(String)
    investitor = Column(String)

    rasporedi = relationship('Raspored', back_populates='gradiliste',cascade='all, delete-orphan')
    karneti = relationship('Karnet', back_populates='gradiliste',cascade='all, delete-orphan')

    def __repr__(self):
        return f"Gradiliste(id={self.id}, naziv={self.naziv})"
    
class Karnet(Base):
    __tablename__ = 'karnet'
    id = Column(Integer, primary_key=True)
    datum = Column(Date)
    prisutan = Column(Boolean)
    sati = Column(Integer)
    zaposleni_id = Column(Integer, ForeignKey('zaposleni.id'))
    gradiliste_id = Column(Integer, ForeignKey('gradiliste.id'))

    zaposleni = relationship('Zaposleni', back_populates='karneti')
    gradiliste = relationship('Gradiliste',back_populates='karneti')

    def __repr__(self):
        return f"Karnet(id={self.id}, datum={self.datum}, sati={self.sati})"
    
class Zaposleni(Base):
    __tablename__ = 'zaposleni'
    id = Column(Integer, primary_key=True)
    ime_prezime = Column(String)
    radno_mesto = Column(String)
    satnica = Column(Float)

    rasporedi = relationship('Raspored', back_populates='zaposleni')
    karneti = relationship('Karnet', back_populates='zaposleni')

    def __repr__(self):
        return f"Zaposleni(id={self.id}, ime={self.ime_prezime})"
    
class Raspored(Base):
    __tablename__ = "raspored"
    id = Column(Integer, primary_key=True)
    zaposleni_id = Column(Integer, ForeignKey('zaposleni.id'))
    gradiliste_id = Column(Integer,ForeignKey('gradiliste.id'))
    datum_od = Column(Date)
    datum_do = Column(Date,nullable=True)
    
    zaposleni=relationship('Zaposleni', back_populates='rasporedi')
    gradiliste=relationship('Gradiliste',back_populates='rasporedi')
