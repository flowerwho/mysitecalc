from models import Gradiliste,Karnet,Zaposleni
from database import session
from datetime import date

#-------------------------------------------------------------------
# 1. CRUD ZA GRADILISTA
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

#-------------------------------------------------------------------
# 1. CRUD ZA ZAPOSLENE

def novi_zaposleni(ime, radno_mesto, satnica):
    novi_radnik = Zaposleni(ime_prezime = ime, radno_mesto = radno_mesto, satnica=satnica)
    session.add(novi_radnik)
    session.commit()
    print("Novi zaposleni je dodat.")

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

def rasporedi_zaposlenog_na_gradiliste(id_zaposlenog, id_gradilista):
    radnik = pronadji_zaposlenog(id_zaposlenog)
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not radnik:
        print("Radnik nije pronadjen.")
        return
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    radnik.gradiliste = gradiliste
    session.commit()

def prikazi_radnike_gradilista(id_gradilista):
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    return gradiliste.radnici

def pronadji_gradiliste_radnika(id_zaposlenog):
    radnik = pronadji_zaposlenog(id_zaposlenog)
    if not radnik :
        print("Zaposleni nije pronadjen.")
        return
    return radnik.gradiliste

#-------------------------------------------------------------------
# 1. CRUD ZA KARNETE
def dodaj_karnet(datum, sati, id_zaposlenog, id_gradilista):
    radnik = pronadji_zaposlenog(id_zaposlenog)
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not radnik: #proverava da li postoji ovaj radnik
        print("Radnik nije pronadjen.")
        return
    if not gradiliste: #proverava da li postoji ovo gradiliste
        print("Gradiliste nije pronadjeno.")
        return
    if datum>date.today():#proverava da li je uneti datum u buducnosti od danasnjeg dana
        print ("Ne mozete uneti sate za dan (datum) u buducnosti.)")
        return
    if not radnik.gradiliste != gradiliste: #proverava da li je radnik rasporedjen na biranom gradilistu
        print("Radnik nije rasporedjen na izabranom gradilistu.")
        return
    if session.query(Karnet).filter_by(zaposleni_id = id_zaposlenog, datum = datum).first(): #proverava da li vec postoje sati za ovog radnika
        print("Za ovog radnika vec postoji unos za taj datum.")
        return
    karnet = Karnet(datum = datum, sati = sati)
    karnet.zaposleni = radnik
    karnet.gradiliste = gradiliste
    session.add(karnet)
    session.commit()

def pronadji_karnet(id_karneta):
    return session.query(Karnet).filter_by(id = id_karneta).first()

def prikazi_sve_karnete():
    return session.query(Karnet).all()

def prikazi_karnete_jednog_radnika(id_radnika):
    zaposleni = pronadji_zaposlenog(id_radnika)
    if not zaposleni:
        print("Radnik nije pronadjen.")
        return
    return zaposleni.karneti

def prikazi_karnete_gradilista(id_gradilista):
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    return gradiliste.karneti

def izmeni_karnet(id_karneta, novi_sati):
    karnet = pronadji_karnet(id_karneta)
    if not karnet:
        print("Karnet nije pronadjen.")
        return
    if (date.today() - karnet.datum).days >5:
        print("Ne mozete izmeniti sate za izabrani datum. Proslo je vise od 5 dana.")
        return
    karnet.sati = novi_sati
    session.commit()

def obrisi_karnet(id_karneta):
    karnet = pronadji_karnet(id_karneta)
    if not karnet:
        print("Karnet nije pronadjen.")
        return
    session.delete(karnet)
    session.commit()


def obracun_plate(id_zaposlenog, mesec, godina):
    zaposleni = pronadji_zaposlenog(id_zaposlenog)
    if not zaposleni:
        print("Radnik nije pronadjen.")
        return
    karneti_zaposlenog = zaposleni.karneti
    if len(karneti_zaposlenog)==0:
        print("Zaposleni nema unete sate u karnet.")
        return
    ukupno_sati = 0
    for karnet in karneti_zaposlenog:
        if (karnet.datum.year == godina and karnet.datum.month == mesec):
            ukupno_sati += karnet.sati
    if ukupno_sati == 0 :
        print("Nema radnik sati za izabrani mesec.")
        return
    bruto_plata = ukupno_sati * zaposleni.satnica
    izvestaj = {"zaposleni ": zaposleni.ime_prezime,
                "mesec: ": mesec,
                "godina ": godina,
                "ukupno sati ":ukupno_sati,
                "satnica ": zaposleni.satnica,
                "plata ": bruto_plata}
    return izvestaj 

def ukupno_sati_gradilista(id_gradilista, mesec, godina):
    gradiliste = pronadji_gradiliste(id_gradilista)
    if not gradiliste:
        print("Gradiliste nije pronadjeno.")
        return
    karneti_gradilista = gradiliste.karneti
    if len(karneti_gradilista) == 0:
        print("Nema unetih sati za birano gradiliste i mesec.")
        return
    ukupno_sati = 0
    for karnet in karneti_gradilista:
        if (karnet.datum.year == godina and karnet.datum.month == mesec):
            ukupno_sati+=karnet.sati
    if ukupno_sati == 0:
        print("Nema unetih sati na ovom gradilistu.")
        return
    izvestaj = {"Gradiliste": gradiliste.naziv,
               "sati gradilista": ukupno_sati}
    return izvestaj


