#presjek segmenata muči float dijeljenje dok se provjerava paralelonst vektora
#edgecase: presjek dviju paralelnih dužina (koliko vrijednosti da vraća)
#! ! ! float vrijednosti

import random
from klase import *
from string import ascii_uppercase
from crtanje import *

#funkcija koja vraća sjecišta zadanih dužina
def presjek_segmenata(duzine):
    sjecista=[]
    br_duzina=len(duzine)
    for i in range(br_duzina):
        for j in range(i + 1, br_duzina):
            S = duzine[i].sjeciste(duzine[j])
            if (S!=Tocka(None,None)):
                sjecista.append(S)
    return sjecista


#funkcija koja vraća sjecišta dane dužine i skupa dužina
def presjek_duzine_i_skupa_duzina(duzina,duzine):
    sjecista=[]
    br_duzina=len(duzine)
    for i in range(br_duzina):
        S = duzina.sjeciste(duzine[i])
        if (S!=Tocka(None,None)):
            sjecista.append(S)
    return sjecista


#--------------------------------------------V I Z U A L I Z A C I J E -------------------------------------------------
#funkcija koja vraća sjecišta zadanih dužina + vizualizacija
def v_presjek_segmenata(duzine):
    sjecista=[]
    br_duzina=len(duzine)

    abeceda = ascii_uppercase

    # stvaranje liste imena točaka i dužina za prikaz
    pom_var1 = 0
    imena_tocaka = [abeceda[i % len(abeceda)] + str(int(pom_var1 := pom_var1 + 1/len(abeceda))) for i in range(br_duzina*2)]
    imena_duzina = [[imena_tocaka[i * 2] + imena_tocaka[i * 2 + 1]] for i in range(br_duzina)]

    for i in range(br_duzina):
        # deklariranje i vizualizacija dužina i točaka koje ih omeđuju
        ax.annotate(imena_tocaka[i * 2], (duzine[i].A.x, duzine[i].A.y))
        ax.scatter(duzine[i].A.x, duzine[i].A.y, marker='.', color='black')
        ax.annotate(imena_tocaka[i * 2+1], (duzine[i].B.x, duzine[i].B.y))
        ax.scatter(duzine[i].B.x, duzine[i].B.y, marker='.', color='black')
        ax.plot([duzine[i].A.x, duzine[i].B.x], [duzine[i].A.y, duzine[i].B.y],label=imena_duzina[i])

        #traženje sjecišta između dviju dužina i njegov prikaz (ako postoji)
        for j in range(i + 1, br_duzina):
            S = duzine[i].sjeciste(duzine[j])
            if (S!=Tocka(None,None)):
                ax.scatter(S.x, S.y, marker='o',color='red')
                sjecista.append(S)

    return sjecista

#TESTNI PRIMJER :
# v_presjek_segmenata([Duzina(Tocka(int(random()*100%20-10),int(random()*100%20-10)),
# Tocka(int(random()*100%20-10),int(random()*100%20-10)))
# for i in range(0,2)])


#funkcija koja vraća sjecišta dane dužine i skupa dužina
def v_presjek_duzine_i_skupa_duzina(duzina,duzine):
    sjecista=[]
    br_duzina=len(duzine)

    abeceda = ascii_uppercase

    # stvaranje liste imena točaka i dužina za prikaz
    pom_var1 = 0
    imena_tocaka = [abeceda[i % len(abeceda)] + str(int(pom_var1 := pom_var1 + 1/len(abeceda))) for i in range(br_duzina * 2+2)]
    imena_duzina = [[imena_tocaka[i * 2] + imena_tocaka[i * 2 + 1]] for i in range(br_duzina+1)]

    # deklariranje i vizualizacija dane dužine i točaka koje ju omeđuju
    ax.annotate(imena_tocaka[0], (duzina.A.x, duzina.A.y))
    ax.scatter(duzina.A.x, duzina.A.y, marker='.', color='black')
    ax.annotate(imena_tocaka[1], (duzina.B.x, duzina.B.y))
    ax.scatter(duzina.B.x, duzina.B.y, marker='.', color='black')
    ax.plot([duzina.A.x, duzina.B.x], [duzina.A.y, duzina.B.y], label=imena_duzina[0])

    for i in range(br_duzina):
        # deklariranje i vizualizacija dužina i točaka koje ih omeđuju
        ax.annotate(imena_tocaka[i*2+2], (duzine[i].A.x, duzine[i].A.y))
        ax.scatter(duzine[i].A.x, duzine[i].A.y, marker='.', color='black')
        ax.annotate(imena_tocaka[i*2+3], (duzine[i].B.x, duzine[i].B.y))
        ax.scatter(duzine[i].B.x, duzine[i].B.y, marker='.', color='black')
        ax.plot([duzine[i].A.x, duzine[i].B.x], [duzine[i].A.y, duzine[i].B.y], label=imena_duzina[0])

        #traženje sjecišta između dviju dužina i njegov prikaz (ako postoji)
        S = duzina.sjeciste(duzine[i])
        if (S!=Tocka(None,None)):
            ax.scatter(S.x, S.y, marker='o', color='red')
            sjecista.append(S)

    return sjecista

#TESTNI PRIMJER :
# v_presjek_duzine_i_skupa_duzina(Duzina(Tocka(int(random()*100%20-10),
# int(random()*100%20-10)),Tocka(int(random()*100%20-10),int(random()*100%20-10)))
# ,[Duzina(Tocka(int(random()*100%20-10),int(random()*100%20-10)),
# Tocka(int(random()*100%20-10),int(random()*100%20-10))) for i in range(0,5)])


#funkcija za testiranje, vraća sjecišta nasumično generiranih dužina
def v_presjek_segmenata_test(br_duzina):
    #generiranje nasumičnih točaka i dužina
    tocke = []
    for i in range(br_duzina):
        A,B=Tocka(int((random.random() * 100) % 20-10), (int(random.random() * 100)%20-10)),Tocka(int((random.random() * 100) % 20-10),(int(random.random() * 100)%20-10))
        while(A==B):
            A, B = Tocka(int((random.random() * 100) % 20 - 10), (int(random.random() * 100) % 20 - 10)), Tocka(
                int((random.random() * 100) % 20 - 10), (int(random.random() * 100) % 20 - 10))
        tocke.append(A)
        tocke.append(B)
    duzine = [Duzina(tocke[i*2],tocke[i*2+1]) for i in range(br_duzina)]

    # stvaranje liste imena točaka i dužina za prikaz
    abeceda = ascii_uppercase
    pom_var1 = 0
    imena_tocaka = [abeceda[i % len(abeceda)] + str(int(pom_var1 := pom_var1 + 1 / len(abeceda))) for i in range(br_duzina*2)]
    imena_duzina = [[imena_tocaka[i * 2] + imena_tocaka[i * 2 + 1]] for i in range(br_duzina)]

    #for petlja u kojoj se određuju sjecista između dvije dužine
    sjecista = []
    for i in range(br_duzina):
        # deklariranje i vizualizacija dužina i točaka koje ih omeđuju
        ax.annotate(imena_tocaka[i * 2], (duzine[i].A.x, duzine[i].A.y))
        ax.scatter(duzine[i].A.x, duzine[i].A.y, marker='.', color='black')
        ax.annotate(imena_tocaka[i * 2 + 1], (duzine[i].B.x, duzine[i].B.y))
        ax.scatter(duzine[i].B.x, duzine[i].B.y, marker='.', color='black')
        ax.plot([duzine[i].A.x, duzine[i].B.x], [duzine[i].A.y, duzine[i].B.y], label=imena_duzina[i])

        # traženje sjecišta između dviju dužina i njegov prikaz (ako postoji)
        for j in range(i + 1, br_duzina):
            S = duzine[i].sjeciste(duzine[j])
            if (S != Tocka(None, None)):
                ax.scatter(S.x, S.y, marker='o', color='red')
                sjecista.append(S)

    return sjecista

#TESTNI PRIMJER :
# v_presjek_segmenata_test(100)

