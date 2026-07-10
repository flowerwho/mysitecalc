from database import session
from datetime import date
from models import Zaposleni, Gradiliste
from crud.gradiliste_crud import *

# 1. CRUD ZA ZAPOSLENE

def novi_zaposleni(ime, radno_mesto, satnica):
    novi_radnik = Zaposleni(ime_prezime = ime, radno_mesto = radno_mesto, satnica=satnica)
    session.add(novi_radnik)
    session.commit()
    return novi_radnik

def prikazi_sve_zaposlene():
    return session.query(Zaposleni).all()

def pronadji_zaposlenog(id_zaposlenog):
    return session.query(Zaposleni).filter_by(id = id_zaposlenog).first()

def promeni_zaposlenog(id_zaposlenog, novo_ime, novo_radno_mesto, nova_satnica):
    zaposleni = pronadji_zaposlenog(id_zaposlenog)
    if not zaposleni:
        print("Radnik nije pronadjen.")
        return
    zaposleni.ime_prezime = novo_ime
    zaposleni.radno_mesto = novo_radno_mesto
    zaposleni.satnica = nova_satnica
    session.commit()

def obrisi_zaposlenog(id_zaposlenog):
    zaposleni = pronadji_zaposlenog(id_zaposlenog)
    if not zaposleni:
        print("Radnik nije pronadjen.")
        return
    session.delete(zaposleni)
    session.commit()


