from models import Gradiliste,Karnet,Zaposleni
from database import session

def dodaj_gradiliste(naziv, lokacija, investitor):
    gradiliste = Gradiliste(naziv=naziv, lokacija = lokacija, investitor = investitor)
    session.add(gradiliste)
    session.commit()
    print("Gradiliste je dodato.")

def prikazi_sva_gradilista():
    return session.query(Gradiliste).all()

def pronadji_gradiliste(id_gradilista):
    return session.query(Gradiliste).filter_by(id = id_gradilista).first()
    

def promeni_gradiliste(id_gradilista, novi_naziv, nova_lokacija, nov_investitor):
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

def novi_zaposleni(ime, radno_mesto, satnica):
    novi_radnik = Zaposleni(ime_prezime = ime, radno_mesto = radno_mesto, satnica=satnica)
    session.add(novi_radnik)
    session.commit()
    print("Novi zaposleni je dodat.")

def dodaj_karnet(datum, sati, id_zaposlenog, id_gradilista):
    zaposleni = session.query(Zaposleni).filter_by(id = id_zaposlenog).first()
    gradiliste = session.query(Gradiliste).filter_by(id = id_gradilista).first()
    if not zaposleni:
        print("Zaposleni nije pronadjen.")
        return
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    karnet = Karnet(datum = datum, sati = sati, zaposleni_id = id_zaposlenog, gradiliste_id = id_gradilista)
    session.add(karnet)
    session.commit()
    print("Karnet je dodat.")

def prikazi_sve_karnete():
    return session.query(Karnet).all()

def prikaz_karneta_jednog_radnika(id_radnika):
    zaposleni = session.query(Zaposleni).filter_by(id = id_radnika).first()
    if not zaposleni:
        print("Nema zaposlenog.")
        return
    return zaposleni.karneti

def obracun_plate(id_zaposlenog, mesec, godina):
    zaposleni = session.query(Zaposleni).filter_by(id = id_zaposlenog).first()
    if not zaposleni:
        print("Zaposleni nije pronadjen.")
        return
    karneti_zaposlenog = zaposleni.karneti
    if not karneti_zaposlenog:
        print("Zaposleni nema unete sate u karnet.")
        return 0
    ukupno_sati = 0
    for karnet in karneti_zaposlenog:
        if (karnet.datum.year == godina and karnet.datum.month == mesec):
            ukupno_sati+=karnet.sati
    plata = ukupno_sati*zaposleni.satnica
    return plata    
    

