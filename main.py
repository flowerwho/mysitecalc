from database import engine,Base
from models import Gradiliste,Zaposleni,Karnet
from crud.gradiliste_crud import *
from crud.karnet_crud import *
from crud.zaposleni_crud import *

Base.metadata.create_all(engine)
print("Baza je kreirana.")




gradiliste = dodaj_gradiliste(
    "Zgrada",
    "Beograd",
    "ZOP"
)