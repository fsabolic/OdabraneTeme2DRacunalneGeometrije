"""Sadrži funkciju za triangulaciju skupa točaka.
"""
from klase import *


def triangulacija(tocke):
    """Vraća listu dužina koje predstavljaju triangulaciju skupa točaka."""
    tocke = list(set(tocke))
    broj_tocaka = len(tocke)

    potencijalne_duzine = []

    for i in range(0, broj_tocaka):
        for j in range(i + 1, broj_tocaka):
            duzina = Duzina(tocke[i], tocke[j])
            potencijalne_duzine.append(duzina)

    potencijalne_duzine.sort(key=lambda duzina: duzina.u_vektor().duljina())

    broj_potencijalnih_duzina = len(potencijalne_duzine)
    duzine_triangulacije = []

    for i in range(0, broj_potencijalnih_duzina):
        potencijalna_duzina = potencijalne_duzine[i]
        postoji_sjeciste = False
        for j in range(0, len(duzine_triangulacije)):
            duzina_triangulacije = duzine_triangulacije[j]
            sjeciste = potencijalna_duzina.sjeciste(duzina_triangulacije)
            if (not sjeciste.prazna()
                    and sjeciste != potencijalna_duzina.A
                    and sjeciste != potencijalna_duzina.B):
                postoji_sjeciste = True

        if not postoji_sjeciste:
            duzine_triangulacije.append(potencijalna_duzina)

    return duzine_triangulacije
