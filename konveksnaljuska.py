from klase import *


def pronadi_indeks_najnize_tocke(tocke):
    br_tocaka = len(tocke)
    indeks_najmanje_tocke = 0

    for i in range(0,br_tocaka):
        if tocke[i].y < tocke[indeks_najmanje_tocke].y:
            indeks_najmanje_tocke = i
        elif (tocke[i].y == tocke[indeks_najmanje_tocke].y
                and tocke[i].x > tocke[indeks_najmanje_tocke].x):
            indeks_najmanje_tocke = i

    return indeks_najmanje_tocke


def konveksna_ljuska(tocke):
    br_tocaka = len(tocke)

    if(br_tocaka<2):
        raise PremaloTocakaError("Premalo točaka za određivanje konv. ljuske")
    elif(br_tocaka==2):
        return tocke

    tocke=list(set(tocke))

    indeks_najnize_tocke = pronadi_indeks_najnize_tocke(tocke)
    najniza_tocka=tocke[indeks_najnize_tocke]

    tocke.pop(indeks_najnize_tocke)
    tocke.sort(key=lambda tocka:(najniza_tocka.polarni_kut(tocka),
                                 tocka.udaljenost_od(najniza_tocka)))
    tocke.append(najniza_tocka)

    n = -1
    tocka_1 = tocke[n]
    tocka_2= tocke[n+1]
    tocka_3 = tocke[n+2]
    while(tocka_3!=najniza_tocka):
        duzina_t1_t2 = Duzina(tocka_1,tocka_2)

        if (tocka_3.lijevo_od(duzina_t1_t2)):
            n+=1
        else:
            tocke.pop(n+1)
            n-=1

        tocka_1 = tocke[n]
        tocka_2 = tocke[n + 1]
        tocka_3 = tocke[n + 2]

    return tocke

