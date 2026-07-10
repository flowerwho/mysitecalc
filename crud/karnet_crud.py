from database import session
from datetime import date
from models import Karnet
from sqlalchemy import extract
from crud.zaposleni_crud import *
from crud.gradiliste_crud import *
from crud.raspored_crud import *

def dodaj_karnet(datum, id_zaposlenog, id_gradilista, prisutan, sati):
    zaposleni = pronadji_zaposlenog(id_zaposlenog)
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not zaposleni:
        print("Zaposleni nije pronadjen.")
        return
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    aktivni_radnici = prikazi_aktivne_radnike_na_gradilistu(id_gradilista,datum)
    if not aktivni_radnici:
        print("Radnik nije rasporedjen na izabranom gradilistu.")
        return
    karnet = Karnet(datum = datum, prisutan = prisutan, sati = sati)
    session.add(karnet)
    session.commit()
    return karnet

def prikazi_karnet_gradilista(id_gradilista,datum):
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    radnici = prikazi_aktivne_radnike_na_gradilistu(id_gradilista, datum)
    rezultat= []
    for radnik in radnici:
        karnet = session.query(Karnet).filter_by(zaposleni_id = radnik.id, gradiliste_id = id_gradilista,datum = datum).first()
        if karnet:
            rezultat.append(karnet)
        else:
            rezultat.append({"radnik":radnik, "prisutan": False, "sati":0})
    return rezultat

def mesecni_karnet_zaposlenog(zaposleni_id, mesec,godina):
    zaposleni = pronadji_zaposlenog(zaposleni_id)
    if not zaposleni:
        print("Zaposleni nije pronadjen.")
        return
    karneti = session.query(Karnet).filter(Karnet.zaposleni_id == zaposleni_id, extract('month', Karnet.datum)==mesec, extract('year',Karnet.datum)==godina).all()
    return karneti
   

def promeni_karnet(id_karneta, novi_sati, prisutan):
    karnet = session.query(Karnet).filter_by(id = id_karneta).first()
    if not karnet:
        print("Karnet nije pronadjen.")
        return
    karnet.sati = novi_sati
    karnet.pristuan = prisutan
    session.commit()
    return karnet

def ukupni_sati_zaposlenog_za_mesec(id_zaposlenog, mesec,godina):
    karneti = mesecni_karnet_zaposlenog(id_zaposlenog,mesec,godina)
    if not karneti:
        return 0
    ukupno = 0
    for k in karneti:
        ukupno += k.sati
    return ukupno

def ukupni_sati_gradilista_za_mesec(id_gradilista,mesec,godina):
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    karneti = session.query(Karnet).filter(Karnet.gradiliste_id == id_gradilista, extract('month', Karnet.datum)==mesec, extract('year', Karnet.datum)==godina).all()
    ukupno = 0
    for k in karneti:
        ukupno += k.sati
    return ukupno

def ukupno_sati_gradilista(id_gradilista):
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    karneti = session.query(Karnet).filter_by(gradiliste_id = id_gradilista).all()
    ukupno = 0
    for k in karneti:
        ukupno+=k.sati
    return ukupno

def prikazi_prisustvo_na_gradilistu(id_gradilista,datum):
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    karneti = session.query(Karnet).filter_by(gradiliste_id = id_gradilista, datum=datum).all()
    prisutni = []
    for k in karneti:
        if k.prisutan:
            prisutni.append(k.zaposleni)
    return prisutni