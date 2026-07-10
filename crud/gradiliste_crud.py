from database import session
from datetime import date
from models import Gradiliste, Raspored

#-------------------------------------------------------------------
# 1. CRUD ZA GRADILISTA
def dodaj_gradiliste(naziv, lokacija, investitor):
    gradiliste = Gradiliste(naziv=naziv, lokacija = lokacija, investitor = investitor)
    session.add(gradiliste)
    session.commit()
    return gradiliste

def prikazi_sva_gradilista():
    return session.query(Gradiliste).all()

def pronadji_gradiliste(id_gradilista):
    return session.query(Gradiliste).filter_by(id = id_gradilista).first()
    

def izmeni_gradiliste(id_gradilista, novi_naziv, nova_lokacija, nov_investitor):
    izabrano_gradiliste = pronadji_gradiliste(id_gradilista)
    if not izabrano_gradiliste:
        print("Gradiliste ne postoji.")
        return
    izabrano_gradiliste.naziv = novi_naziv
    izabrano_gradiliste.lokacija = nova_lokacija
    izabrano_gradiliste.investitor = nov_investitor
    session.commit()

def obrisi_gradiliste(id_gradilista):
    trazeno_gradiliste = pronadji_gradiliste(id_gradilista)
    if not trazeno_gradiliste:
        print("Gradiliste ne postoji.")
        return
    session.delete(trazeno_gradiliste)
    session.commit()

def radnici_na_gradilistu(id_gradilista, datum):
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    lista_radnika =[]
    for r in gradiliste.rasporedi:
        if r.datum_od<=datum:
            if r.datum_do is None or datum<= r.datum_do:
                lista_radnika.append(r.zaposleni)
    return lista_radnika

def broj_radnika_na_gradilistu(id_gradilista,datum):
    radnici = radnici_na_gradilistu(id_gradilista,datum)
    if radnici is None :
        return
    return len(radnici)
