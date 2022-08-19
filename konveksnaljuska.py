#ne radi ako se radi SAMO o skupu točaka koje se sve nalaze na 1 liniji
#ŠTO SA TOČKAMA KOJE SE NALAZE NA DUŽINI IZMEĐU 2 TOČKE KONVEKSNE LJUSKE
from klase import *
import random
import matplotlib.pyplot as plt

# Grahamov scan!
#prvo izbacujemo sve iste točke (mogu nastati problemi zbog zadavanja dužina s istim točkama i sl.)
#nakon toga određujemo točku P0 koja ima najmanju ordinatu na temelju koje ćemo sortirati ostale točke
#točku P0 s najmanjom ordinatom izbacujemo iz skupa točaka kako bi se izbjegle greške sa zadavanjem dužina s istim točkama (ovo je edgecase samo)
#točke sortiramo prema polarnom kutu koja dana točka Pi ima s točkom P0 (odnosno dužina 'PiP0' s dužinom 'P0,P0+(1,1)'), a ako je polarni kut za dvije točke jednak, gleda se njihova udaljenost od točke P0
#nakon toga, pokušavamo pronaći točke koje čine konveksnu ljusku
#konveksnu ljusku pronalazimo tako da uzimamo točku P0 kao početnu točku (jer je ona sigurno točka u konveksnoj ljuski)
#nakon toga uzimamo po redu 3 točke (p1,p2,p3) i gledamo koji je kut između njih, ako je on između 0 i 180 stupnjeva, tada je on skretanje u lijevo, a ako je veći od 180, a manji od 360 tada je on skretanje udesno
#svakim skretanjem udesno izbacujemo točku p2, a skretanjem ulijevo pomičemo se u listi sortiranih točaka za jedno mjesto
# [Computational Geometry - An Introduction, 106. str]
def konveksna_ljuska(tocke):
    if(len(tocke)<2):
        raise ValueError ('Premalo točaka za određivanje konveksne ljuske')
    if((len(tocke)==2)):
        return tocke

    tocke=list(set(tocke))

    najmanja = tocke[0]
    for i in tocke:
        if i.y < najmanja.y:
            najmanja = i
        elif i.y == najmanja.y and i.x > najmanja.x:
            najmanja = i
    P0=najmanja
    tocke=[i for i in tocke if i!=P0]

    l=sorted(tocke, key=lambda x:(Duzina(P0,P0+Tocka(1,0)).u_vektor().kut_izmedu_vektora(Duzina(P0,Tocka(x.x,x.y)).u_vektor()),Duzina(P0,x).u_vektor().duljina()))
    l.append(P0)

    p1,p2,p3=-1,0,1
    while(l[p3]!=l[-1]):
        u = Duzina(l[p2], l[p1]).u_vektor()
        v = Duzina(l[p2], l[p3]).u_vektor()

        if (v.vektorski_produkt(u) <= 0): #ovdje sam uklonio <= i stavio samo < jer mi tak onda ulovi i kolinearne točke, ako nešta ne radi, probaj ovo vratit na <=
            l = [i for i in l if i != l[p2]]
            p1,p2,p3=p1-1,p2-1,p3-1
        else:
            p1,p2,p3=p1+1,p2+1,p3+1

    return l

#--------------------------------------------V I Z U A L I Z A C I J E -------------------------------------------------

def v_konveksna_ljuska(tocke):
    k_l=konveksna_ljuska(tocke)
    plt.fill([i.x for i in k_l], [i.y for i in k_l], facecolor="lightblue", edgecolor="blue")
    plt.scatter([i.x for i in tocke], [i.y for i in tocke], color="black")
    plt.scatter([i.x for i in k_l], [i.y for i in k_l], color="red")
    plt.show()
    return k_l

def v_konveksna_ljuska_test(br_tocaka):
    tocke=[Tocka(random.random()*1000%20-10,random.random()*1000%20-10) for i in range(br_tocaka)]
    k_l=v_konveksna_ljuska(tocke)