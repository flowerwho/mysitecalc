from database import session
from datetime import date
from models import Zaposleni, Gradiliste
from crud.gradiliste_crud import *
from crud.zaposleni_crud import *


def rasporedi_zaposlenog_na_gradiliste(id_zaposlenog, id_gradilista,od_datuma):
    zaposleni = pronadji_zaposlenog(id_zaposlenog)
    if not zaposleni:
        print("Zaposleni nije pronadjen.")
        return
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    raspored = Raspored(zaposleni_id = id_zaposlenog, gradiliste_id = id_gradilista, datum_od = od_datuma)
    session.add(raspored)
    session.commit()
    return raspored

def pronadji_raspored(id_rasporeda):
    return session.query(Raspored).filter_by(id = id_rasporeda).first()
    


def prikazi_aktivne_radnike_na_gradilistu(id_gradilista, datum):
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    rasporedi = gradiliste.rasporedi
    radnici = []
    for r in rasporedi:
        if r.datum_od<=datum:
            if r.datum_do is None or datum<=r.datum_do:
                radnici.append(r.zaposleni)
    return radnici                           

def promeni_gradiliste_zaposlenom(id_zaposlenog, id_novog_gradilista, datum_promene):
    zaposleni = pronadji_zaposlenog(id_zaposlenog)
    if not zaposleni:
        print("Zaposleni nije pronadjen.")
        return
    novo_gradiliste = pronadji_gradiliste(id_novog_gradilista)
    if not novo_gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    #pronalazimo trenutni aktivni raspored
    aktivni_raspored = None
    for r in zaposleni.rasporedi:
        if r.datum_do is None:
            aktivni_raspored = r
            break
    #zatvaramo stari raspored
    if aktivni_raspored:
        aktivni_raspored.datum_do = datum_promene
    #pravimo novi raspored
    novi_raspored = Raspored(zaposleni_id = id_zaposlenog, gradiliste_id = id_novog_gradilista, datum_od = datum_promene)
    session.add(novi_raspored)
    session.commit()
    return novi_raspored

def zavrsi_raspored_radnika(id_zaposlenog, datum):
    zaposleni = pronadji_zaposlenog(id_zaposlenog)
    if not zaposleni:
        print("Zaposleni nije pronadjen.")
        return
    aktivni_raspored = None
    for r in zaposleni.rasporedi:
        if r.datum_do is None:
            aktivni_raspored = r
            break
    if aktivni_raspored:
        aktivni_raspored.datum_do = datum
    session.commit()


