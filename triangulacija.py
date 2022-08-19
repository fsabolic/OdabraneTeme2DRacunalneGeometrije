from klase import *
from voronoi import v_voronoi
import matplotlib.pyplot as plt
#Ovo je "pohlepna" implementacija triangulacije
#Prvo nađemo sve dužine koje mogu postojati između točaka u danom skupu točaka
# Nakon toga, sortiramo ih po duljini
# Na kraju, po redu uzimamo dužine i pohranjujemo ih kao dijelove triangulacije, osim ako postoji sjecište između odabrane dužine i neke dužine koja se nalazi u skupu već odabranih dužina
# [Computational Geometry - An Introduction, 235. str]

def triangulacija(tocke):
    tocke = list(set(tocke))

    duzine = []

    for i in range(0, len(tocke)):
        for j in range(i + 1, len(tocke)):
            duzine.append(Duzina(tocke[i], tocke[j]))

    duzine.sort(key=lambda duzina: duzina.u_vektor().duljina())

    triang_duzine = []

    for i in range(0, len(duzine)):
        postoji_sjeciste = False
        for j in range(0, len(triang_duzine)):
            if (not duzine[i].sjeciste(triang_duzine[j]).prazna() and duzine[i].sjeciste(triang_duzine[j]) != duzine[
                i].A and duzine[i].sjeciste(triang_duzine[j]) != duzine[i].B):
                postoji_sjeciste = True

        if (not postoji_sjeciste):
            triang_duzine.append(duzine[i])

    return triang_duzine

def v_triangulacija(tocke):
    triang_duzine = triangulacija(tocke)

    for duzina in triang_duzine:
        plt.plot([duzina.A.x,duzina.B.x],[duzina.A.y,duzina.B.y],color="black",linestyle="dashed")

    for tocka in tocke:
        plt.scatter(tocka.x, tocka.y, color="red",marker="x")
    plt.show()
    return triang_duzine

def v_triangulacija_test(br_tocaka):

    tocke = [Tocka(generiraj_broj(),generiraj_broj()) for i in range(0,br_tocaka)]

    triang_duzine = v_triangulacija(tocke)


def v_triangulacija_voronoi_test(br_tocaka):
    tocke = [Tocka(generiraj_broj(), generiraj_broj()) for i in range(0, br_tocaka)]

    triang_duzine = triangulacija(tocke)

    for duzina in triang_duzine:
        plt.plot([duzina.A.x,duzina.B.x],[duzina.A.y,duzina.B.y],color="black",linestyle="dotted")

    for tocka in tocke:
        plt.scatter(tocka.x, tocka.y, color="red",marker="x")
    v_voronoi(tocke)