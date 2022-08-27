"""Sadrži funkcije za određivanje konveksne ljuske.

Modul sadrži implementaciju Graham Scan algoritma za traženje konveksne
ljuske.


"""
from klase import *
from iznimke import PremaloTocakaError


def pronadi_indeks_najnize_tocke(tocke):
    """Pronalazi indeks točke s najmanjom oridnatom u listi."""
    br_tocaka = len(tocke)
    indeks_najmanje_tocke = 0

    for i in range(0, br_tocaka):
        if tocke[i].y < tocke[indeks_najmanje_tocke].y:
            indeks_najmanje_tocke = i
        elif (tocke[i].y == tocke[indeks_najmanje_tocke].y
                and tocke[i].x > tocke[indeks_najmanje_tocke].x):
            indeks_najmanje_tocke = i

    return indeks_najmanje_tocke


def konveksna_ljuska(tocke):
    """Vraća konveksnu ljusku za listu točaka.

    Implementacija Graham Scan algoritma.

    Parametri
    ---------
    tocke: lista Tocaka

    Vraća
    -----
    tocke: lista Tocaka

    Iznimke:
    PremaloTocakaError
        Konveksnu ljusku nije moguće odrediti za manje od dvije točke.
    """
    br_tocaka = len(tocke)

    if br_tocaka < 2:
        raise PremaloTocakaError("Premalo točaka za određivanje konv. ljuske")
    if br_tocaka == 2:
        return tocke

    tocke = list(set(tocke))

    indeks_najnize_tocke = pronadi_indeks_najnize_tocke(tocke)
    najniza_tocka = tocke[indeks_najnize_tocke]

    tocke.pop(indeks_najnize_tocke)
    tocke.sort(key=lambda tocka: (najniza_tocka.polarni_kut(tocka),
                                  tocka.udaljenost_od(najniza_tocka)))
    tocke.append(najniza_tocka)

    indeks_n = -1
    tocka_1 = tocke[indeks_n]
    tocka_2 = tocke[indeks_n + 1]
    tocka_3 = tocke[indeks_n + 2]
    while tocka_3 != najniza_tocka:
        duzina_t1_t2 = Duzina(tocka_1, tocka_2)

        if tocka_3.lijevo_od(duzina_t1_t2):
            indeks_n += 1
        else:
            tocke.pop(indeks_n + 1)
            indeks_n -= 1

        tocka_1 = tocke[indeks_n]
        tocka_2 = tocke[indeks_n + 1]
        tocka_3 = tocke[indeks_n + 2]

    return tocke
