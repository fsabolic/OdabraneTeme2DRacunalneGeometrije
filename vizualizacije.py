"""Sadrži funkcije za vizualizaciju i testiranje algoritama ostalih modula.

Modul sadrži nekoliko funkcija za izradu objekata klasa s nasumičnim
vrijednostima u svrhu testiranja. Za određeni skup algoritama implementirane
su vizualizacije za koje se mogu zadati parametri algoritma i funkcije za
testiranje algoritama.

"""

import random
import matplotlib.pyplot as plt
from klase import *
from presjeksegmenata import presjek_segmenata
from konveksnaljuska import konveksna_ljuska
from voronoi import voronoi
from triangulacija import triangulacija


def generiraj_broj(maks=10):
    """Generira nasumični broj u rasponu [-maks,maks].

    Parametri
    ---------
    maks: int, opcionalan

    Vraća
    -----
    :int
    """
    return random.random() * 1000 % 2 * maks - maks


def nasumicna_tocka(maks=10):
    """Vraća nasumično generiran objekt klase Tocka."""
    return Tocka(generiraj_broj(maks), generiraj_broj(maks))


def nasumicne_tocke(broj_tocaka, maks=10):
    """Vraća nasumično generiranu listu objekata klase Tocka."""
    tocke = []
    while (len(tocke) < broj_tocaka and len(
            tocke) != (2 * maks - 1) * (2 * maks - 1)):
        tocke.append(nasumicna_tocka(maks))
        tocke = list(set(tocke))
    return tocke


def nasumicna_duzina(maks=10):
    """Vraća nasumično generiran objekt klase Duzina."""
    A = nasumicna_tocka(maks)
    B = nasumicna_tocka(maks)
    while A == B:
        B = nasumicna_tocka(maks)

    return Duzina(A, B)


def nasumicne_duzine(broj_duzina, maks=10):
    """Vraća nasumično generiranu listu objekata klase Duzina."""
    duzine = []
    while len(duzine) < broj_duzina:
        duzine.append(nasumicna_duzina(maks))
        duzine = list(set(duzine))
    return duzine


def nasumicni_poligon(broj_vrhova, maks=10):
    """Vraća nasumično generiran objekt klase Poligon."""
    return Poligon(nasumicne_tocke(broj_vrhova, maks))


def nacrtaj_tocku(tocka, boja=None, marker=None):
    """Prikazuje točku pomoću matplotbib paketa.

    Parametri
    ---------
    tocka: Tocka
        Točka za prikazati.
    boja: string, opcionalan
        Boja nacrtane točke.
    marker: string, opcionalan
        Prikaz točke.
    """
    plt.scatter(tocka.x, tocka.y, color=boja, marker=marker, zorder=3)


def nacrtaj_tocke(tocke, boja=None, marker=None):
    """Prikazuje skup točaka pomoću matplotbib paketa.

    Parametri
    ---------
    tocke: lista Tocaka
        Točke za prikazati.
    boja: string, opcionalan
        Boja nacrtanih točaka.
    marker: string, opcionalan
        Prikaz točaka.
    """
    for tocka in tocke:
        nacrtaj_tocku(tocka, boja, marker)


def nacrtaj_duzinu(duzina, boja=None, debljina=None):
    """Prikazuje dužinu pomoću matplotbib paketa.

    Parametri
    ---------
    duzina: Duzina
        Dužina za prikazati.
    boja: string, opcionalan
        Boja nacrtane dužine.
    debljina: string, opcionalan
        Debljina prikazane dužine.
    """
    plt.plot([duzina.A.x, duzina.B.x],
             [duzina.A.y, duzina.B.y],
             color=boja,
             linewidth=debljina,
             zorder=2
             )


def nacrtaj_duzine(duzine, boja=None, debljina=None):
    """Prikazuje skup dužina pomoću matplotbib paketa.

    Parametri
    ---------
    duzine: lista Duzina
        Dužine za prikazati.
    boja: string, opcionalan
        Boja nacrtanih dužina.
    debljina: string, opcionalan
        Debljina prikazanih dužina.
    """
    for duzina in duzine:
        nacrtaj_duzinu(duzina, boja, debljina)


def nacrtaj_poligon(poligon,
                    boja_poligona=None,
                    boja_rubova=None,
                    transparentnost=None
                    ):
    """Prikazuje poligon pomoću matplotbib paketa.

    Parametri
    ---------
    poligon: Poligon
        Poligon za prikazati.
    boja_poligona: string, opcionalan

    boja_rubova: string, opcionalan

    transparentnost: string, opcionalan
    """
    poligon = poligon.vrhovi
    plt.fill([vrh.x for vrh in poligon],
             [vrh.y for vrh in poligon],
             facecolor=boja_poligona,
             edgecolor=boja_rubova,
             alpha=transparentnost, zorder=1
             )


def v_presjek_segmenata(duzine):
    """Vizualizacija presjeka skupa dužina."""
    nacrtaj_duzine(duzine, None, 2)

    sjecista = presjek_segmenata(duzine)
    nacrtaj_tocke(sjecista, "red")

    plt.show()


def v_tocka_u_poligonu(tocke, poligon):
    """Vizualizacija položaja točke u odnosu sa poligonom. (Ray Casting algoritam)"""
    nacrtaj_poligon(poligon, "lightblue", "blue")
    nacrtaj_tocke(poligon.vrhovi, "blue")
    for tocka in tocke:
        pripada = tocka.pripada_poligonu(poligon)
        if pripada == 1:
            nacrtaj_tocku(tocka, "red")
        elif pripada == 0:
            nacrtaj_tocku(tocka, "green")
        else:
            nacrtaj_tocku(tocka, "black")

    plt.show()


def v_tocka_u_poligonu_wn(tocke, poligon):
    """Vizualizacija položaja točke u odnosu sa poligonom. (Winding Number algoritam)"""
    nacrtaj_poligon(poligon, "lightblue", "blue")
    nacrtaj_tocke(poligon.vrhovi, "blue")

    for tocka in tocke:
        pripada = tocka.pripada_poligonu_wn(poligon)
        if pripada == 1:
            nacrtaj_tocku(tocka, "red")
        elif pripada == 0:
            nacrtaj_tocku(tocka, "green")
        else:
            nacrtaj_tocku(tocka, "black")

    plt.show()


def v_konveksna_ljuska(tocke):
    """Vizualizacija konveksne ljuske skupa točaka."""
    tocke_ljuske = konveksna_ljuska(tocke)
    poligon_ljuske = Poligon(tocke_ljuske)

    nacrtaj_poligon(poligon_ljuske, "lightblue", "blue")
    nacrtaj_tocke(tocke, "black")
    nacrtaj_tocke(tocke_ljuske, "red")

    plt.show()


def v_unija(p_1, p_2):
    """Vizualizacija unije dvaju poligona."""
    unija = p_1 + p_2

    nacrtaj_poligon(p_1, "lightblue", "none", 0.6)
    nacrtaj_poligon(p_2, "pink", "none", 0.5)

    for poligon in unija:
        nacrtaj_poligon(poligon, "none", "black")
        nacrtaj_tocke(poligon.vrhovi, "black")

    plt.show()


def v_razlika(p_1, p_2):
    """Vizualizacija razlike dvaju poligona."""
    razlika = p_1 - p_2

    nacrtaj_poligon(p_2, "orangered", "red", 0.35)
    nacrtaj_poligon(p_1, "lightblue", "blue", 0.35)

    for poligon in razlika:
        nacrtaj_poligon(poligon, "lightblue", "black", 0.75)
        nacrtaj_tocke(poligon.vrhovi, "black")

    plt.show()


def v_presjek(p_1, p_2):
    """Vizualizacija presjeka dvaju poligona."""
    presjek = p_1 * p_2

    nacrtaj_poligon(p_2, "blue", "none", 0.4)
    nacrtaj_poligon(p_1, "red", "none", 0.4)

    for poligon in presjek:
        nacrtaj_poligon(poligon, "violet", "black")
        nacrtaj_tocke(poligon.vrhovi, "black")

    plt.show()


def v_triangulacija(tocke):
    """Vizualizacija triangulacije skupa točaka."""
    triang_duzine = triangulacija(tocke)

    nacrtaj_duzine(triang_duzine, "dimgray")
    nacrtaj_tocke(tocke, "crimson")

    plt.show()


def v_voronoi(tocke):
    """Vizualizacija izrade Voronojevog dijagrama za skup točaka."""
    celije_dijagrama = voronoi(tocke)

    for celija in celije_dijagrama:
        vrhovi_poligona = celija.poligon.vrhovi
        plt.fill([vrh.x for vrh in vrhovi_poligona],
                 [vrh.y for vrh in vrhovi_poligona],
                 alpha=0.15)

        nacrtaj_duzine(celija.poligon.rubovi(), "black")

    nacrtaj_tocke(tocke, "red", ".")

    min_koordinata = max([abs(tocka.x) for tocka in tocke]
                         + [abs(tocka.y) for tocka in tocke]) * 1.1

    plt.axis([-min_koordinata, min_koordinata, -min_koordinata, min_koordinata])
    plt.show()


def v_presjek_segmenata_test(br_duzina):
    """Vizualizira presjek skupa dužina za dani broj nasumičnih dužina."""
    duzine = nasumicne_duzine(br_duzina, 1000)
    v_presjek_segmenata(duzine)


def v_tocka_u_poligonu_test(br_tocaka):
    """Vizualizira položaj nasumičnih točaka u odnosu na nasumični poligon za dani broj točaka.

    Ray Casting algoritam.
    """
    tocke = nasumicne_tocke(br_tocaka)
    poligon = nasumicni_konveksni_poligon()
    v_tocka_u_poligonu(tocke, poligon)
    plt.show()


def v_tocka_u_poligonu_wn_test(br_tocaka):
    """Vizualizira položaj nasumičnih točaka u odnosu na nasumični poligon za dani broj točaka.

    Winding Number algoritam.
    """
    tocke = nasumicne_tocke(br_tocaka)
    poligon = nasumicni_konveksni_poligon()
    v_tocka_u_poligonu(tocke, poligon)
    plt.show()


def v_konveksna_ljuska_test(br_tocaka):
    """Vizulizira konveksnu ljusku za dani broj nasumičnih točaka."""
    tocke = nasumicne_tocke(br_tocaka)
    v_konveksna_ljuska(tocke)


def v_razlika_test():
    """Vizualizira razliku dvaju nasumičnih konveksnih poligona."""
    p_1 = nasumicni_konveksni_poligon()
    p_2 = nasumicni_konveksni_poligon()
    v_razlika(p_1, p_2)


def v_unija_test():
    """Vizualizira uniju dvaju nasumičnih konveksnih poligona."""
    p_1 = nasumicni_konveksni_poligon()
    p_2 = nasumicni_konveksni_poligon()
    v_unija(p_1, p_2)


def v_presjek_test():
    """Vizualizira presjek dvaju nasumičnih konveksnih poligona."""
    p_1 = nasumicni_konveksni_poligon()
    p_2 = nasumicni_konveksni_poligon()
    v_presjek(p_1, p_2)


def v_triangulacija_test(br_tocaka):
    """Vizualizira triangulaciju za dani broj nasumičnih točaka."""
    tocke = nasumicne_tocke(br_tocaka)

    v_triangulacija(tocke)


def v_triangulacija_voronoi_test(br_tocaka):
    """Vizualizira triangulaciju i izradu Voronojevog dijagrama za dani broj nasumičnih točaka"""
    tocke = nasumicne_tocke(br_tocaka)
    triang_duzine = triangulacija(tocke)

    nacrtaj_duzine(triang_duzine, "dimgray")

    celije_dijagrama = voronoi(tocke)

    for celija in celije_dijagrama:
        vrhovi_poligona = celija.poligon.vrhovi
        plt.fill([vrh.x for vrh in vrhovi_poligona],
                 [vrh.y for vrh in vrhovi_poligona],
                 alpha=0.15)

        nacrtaj_duzine(celija.poligon.rubovi(), "black")

    nacrtaj_tocke(tocke, "red", ".")

    min_koordinata = max([abs(tocka.x) for tocka in tocke]
                         + [abs(tocka.y) for tocka in tocke]) * 1.1

    plt.axis([-min_koordinata,
              min_koordinata,
              -min_koordinata,
              min_koordinata])
    plt.show()


def v_voronoi_test(broj_tocaka):
    """Vizualizira izradu Voronojevog dijagrama za dani broj nasumičnih točaka"""
    tocke = nasumicne_tocke(broj_tocaka)
    v_voronoi(tocke)


def nasumicni_konveksni_poligon():
    """Vraća nasumični konveksni poligon."""
    poligon = nasumicni_poligon(abs(generiraj_broj()) + 3).vrhovi
    return Poligon(konveksna_ljuska(poligon))
