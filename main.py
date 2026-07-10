from datetime import date, timedelta

from database import engine, Base

from models import Gradiliste, Zaposleni, Karnet

from crud.gradiliste_crud import *
from crud.zaposleni_crud import *
from crud.karnet_crud import *



# KREIRANJE TABELE
Base.metadata.create_all(engine)



