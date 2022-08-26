from konveksnaljuska import *
from presjeksegmenata import *
from voronoi import *
from triangulacija import *
import matplotlib.pyplot as plt

def nacrtaj_tocku(tocka,boja=None,marker=None):
    plt.scatter(tocka.x, tocka.y, color=boja, marker=marker,zorder=3)


def nacrtaj_tocke(tocke,boja=None,marker=None):
    for tocka in tocke:
        nacrtaj_tocku(tocka,boja,marker)


def nacrtaj_duzinu(duzina,boja=None,debljina=None):
    plt.plot([duzina.A.x, duzina.B.x],
             [duzina.A.y, duzina.B.y],
             color=boja,
             linewidth=debljina,
             zorder=2
             )


def nacrtaj_duzine(duzine,boja=None,debljina=None):
    for duzina in duzine:
        nacrtaj_duzinu(duzina,boja)


def nacrtaj_poligon(poligon,
                    boja_poligona=None,
                    boja_rubova=None,
                    transparentnost=None
                    ):
    poligon=poligon.vrhovi
    plt.fill([vrh.x for vrh in poligon],
             [vrh.y for vrh in poligon],
             facecolor=boja_poligona,
             edgecolor=boja_rubova,
             alpha=transparentnost,zorder=1
             )


def v_presjek_segmenata(duzine):
    nacrtaj_duzine(duzine,None,2)

    sjecista = presjek_segmenata(duzine)
    nacrtaj_tocke(sjecista,"red")

    plt.show()


def v_tocka_u_poligonu(tocke,poligon):
    nacrtaj_poligon(poligon,"lightblue","blue")
    nacrtaj_tocke(poligon.vrhovi,"blue")
    for tocka in tocke:
        pripada = tocka.pripada_poligonu(poligon)
        if(pripada==1):
            nacrtaj_tocku(tocka,"red")
        elif(pripada==0):
            nacrtaj_tocku(tocka,"green")
        else:
            nacrtaj_tocku(tocka,"black")

    plt.show()


def v_tocka_u_poligonu_wn(tocke,poligon):
    nacrtaj_poligon(poligon,"lightblue","blue")
    nacrtaj_tocke(poligon.vrhovi,"blue")

    for tocka in tocke:
        pripada = tocka.pripada_poligonu_wn(poligon)
        if(pripada==1):
            nacrtaj_tocku(tocka,"red")
        elif(pripada==0):
            nacrtaj_tocku(tocka,"green")
        else:
            nacrtaj_tocku(tocka,"black")

    plt.show()


def v_konveksna_ljuska(tocke):
    tocke_ljuske=konveksna_ljuska(tocke)
    poligon_ljuske = Poligon(tocke_ljuske)

    nacrtaj_poligon(poligon_ljuske,"lightblue","blue")
    nacrtaj_tocke(tocke,"black")
    nacrtaj_tocke(tocke_ljuske,"red")

    plt.show()


def v_unija(p_1,p_2):
    unija  = p_1+p_2

    nacrtaj_poligon(p_1,"lightblue","none",0.6)
    nacrtaj_poligon(p_2,"pink","none",0.5)

    for poligon in unija:
        nacrtaj_poligon(poligon,"none","black")
        nacrtaj_tocke(poligon.vrhovi,"black")

    plt.show()

def v_razlika(p_1,p_2):
    razlika = p_1 - p_2

    nacrtaj_poligon(p_2,"orangered","red",0.35)
    nacrtaj_poligon(p_1,"lightblue","blue",0.35)

    for poligon in razlika:
        nacrtaj_poligon(poligon,"lightblue","black",0.75)
        nacrtaj_tocke(poligon.vrhovi,"black")

    plt.show()

def v_presjek(p_1,p_2):
    presjek = p_1*p_2

    nacrtaj_poligon(p_2,"blue","none",0.4)
    nacrtaj_poligon(p_1,"red","none",0.4)

    for poligon in presjek:
        nacrtaj_poligon(poligon,"violet","black")
        nacrtaj_tocke(poligon.vrhovi,"black")

    plt.show()


def v_triangulacija(tocke):
    triang_duzine = triangulacija(tocke)

    nacrtaj_duzine(triang_duzine,"dimgray")
    nacrtaj_tocke(tocke,"crimson")

    plt.show()

def v_voronoi(tocke):
    celije_dijagrama = voronoi(tocke)


    for celija in celije_dijagrama:
        vrhovi_poligona = celija.Poligon.vrhovi
        plt.fill([vrh.x for vrh in vrhovi_poligona],
                 [vrh.y for vrh in vrhovi_poligona],
                 alpha=0.15)

        nacrtaj_duzine(celija.Poligon.rubovi(),"black")

    nacrtaj_tocke(tocke,"red",".")

    min_koordinata = max([abs(tocka.x) for tocka in tocke]
                         +[abs(tocka.y) for tocka in tocke])*1.1

    plt.axis([-min_koordinata,min_koordinata,-min_koordinata,min_koordinata])
    plt.show()

def v_presjek_segmenata_test(br_duzina):
    duzine = nasumicne_duzine(br_duzina,1000)
    v_presjek_segmenata(duzine)

def v_tocka_u_poligonu_test(br_tocaka):
    tocke = nasumicne_tocke(br_tocaka)
    poligon = nasumicni_konveksni_poligon()
    v_tocka_u_poligonu(tocke,poligon)
    plt.show()

def v_tocka_u_poligonu_wn_test(br_tocaka):
    tocke = nasumicne_tocke(br_tocaka)
    poligon = nasumicni_konveksni_poligon()
    v_tocka_u_poligonu(tocke,poligon)
    plt.show()

def v_konveksna_ljuska_test(br_tocaka):
    tocke= nasumicne_tocke(br_tocaka)
    v_konveksna_ljuska(tocke)



def v_razlika_test():
   p1 = nasumicni_konveksni_poligon()
   p2 = nasumicni_konveksni_poligon()
   v_razlika(p1,p2)

def v_unija_test():
   p1 = nasumicni_konveksni_poligon()
   p2 = nasumicni_konveksni_poligon()
   v_unija(p1,p2)

def v_presjek_test():
   p1 = nasumicni_konveksni_poligon()
   p2 = nasumicni_konveksni_poligon()
   v_presjek(p1,p2)



def v_triangulacija_test(br_tocaka):

    tocke = nasumicne_tocke(br_tocaka)

    v_triangulacija(tocke)

def v_triangulacija_voronoi_test(br_tocaka):
    tocke = nasumicne_tocke(br_tocaka)
    triang_duzine = triangulacija(tocke)

    nacrtaj_duzine(triang_duzine, "dimgray")

    celije_dijagrama = voronoi(tocke)

    for celija in celije_dijagrama:
        vrhovi_poligona = celija.Poligon.vrhovi
        plt.fill([vrh.x for vrh in vrhovi_poligona],
                 [vrh.y for vrh in vrhovi_poligona],
                 alpha=0.15)

        nacrtaj_duzine(celija.Poligon.rubovi(), "black")

    nacrtaj_tocke(tocke, "red", ".")

    min_koordinata = max([abs(tocka.x) for tocka in tocke]
                         + [abs(tocka.y) for tocka in tocke]) * 1.1

    plt.axis([-min_koordinata,
              min_koordinata,
              -min_koordinata,
              min_koordinata])
    plt.show()



def v_voronoi_test(broj_tocaka):

    tocke=nasumicne_tocke(broj_tocaka)
    v_voronoi(tocke)


def nasumicni_konveksni_poligon():
    poligon = nasumicni_poligon(abs(generiraj_broj()) + 3).vrhovi
    return Poligon(konveksna_ljuska(poligon))