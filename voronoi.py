import matplotlib.pyplot as plt
from presjeksegmenata import *
from booloperacije import *
from konveksnaljuska import *
import math

#Prvo uklanjamo duplikatne točke u danom skupu
#Ako su zadane samo dvije točke, koristimo poseban algoritam koji stvara samo jednu simetralu i dijeli prostor na dva četverokuta:
    #Prvo stvaramo simetralu dužine koju čine dane dvije točke
    #Nakon toga zadajemo 4 točke koje su proizvoljno daleko od središta koordinatnog sustava
    #Određujemo na kojoj strani se nalazi jedna od točaka zadanih u skupu točaka
    #Prvi poligon (buduću ćeliju dijagrama) će činiti točke simetrale i sve granične točke koje se nalaze na istoj strani kao odabrana točka simetrale
    #Kako bismo dobili poligon, sortiramo točke na temelju polarnog kuta
    #Postupak za drugi poligon je identičan, osim što u njega spremamo granične točke sa suprotne strane
#Cilj je za svaku točku pronaći sve simetrale koje čine njihove dužine sa svim ostalim točkama u skupu. Te simetrale i njihova sjecišta činiti će poligon, odnosno Voronojevu ćeliju
#Prvo sortiramo sve točke po udaljenosti od trenutne točke koju promatramo. To radimo kako bi šro prije pronašli poligon/ćeliju
#Za svaku točku u skupu pronalazimo simetralu dužine koja ona čini s trenutnom točkom
#Ukoliko smo našli simetralu s prvom točkom, odmah ju spremamo kao jedan rub poligona
#U suprotnome, prvo tražimo sjecište između postojećih rubova i trenutne simetrale koju promatramo
 #Ako postoji sjecište, znači da trenutna simetrala dijeli postojeći rub na dva dijela kao što i postojeći rub dijeli trenutnu simetralu na dva dijela
 # Iznimno, može se desiti da se trenutna simetrala i postojeći rub sjeku u nekoj krajnjoj točci
     # Ako trenutna simetrala sjeće postojeći rub u krajnjoj točci, tada će postojeći rub ostati u listi točnih rubova Voronojeve ćelije
#U suprotnome, uklanjamo cijeli postojeći rub (jer neće cijeli rub činiti stranicu ćelije, već samo jedan od njena dva dijela)
#Rub se dijeli na dio od točke A do sjecišta i od sjecišta do točke B
#Za početak predstavljamo da je "lijeva polovica" točna polovica koja će činiti rub Voronojeve ćelije (zapravo nema lijeve i desne polovice, samo se tako nazivaju)
# Kako bi pronašli koja polovica je "točna" (čini rub Voronojeve ćelije), promatramo koliki kut zatvaraju vektori koje čine dijelovi ruba s vektorom od sjecišta do trenutne točke
# Što je kut između vektora manji, to je trenutna točka "bliže" određenom dijelu ruba. Zapravo gledamo koliko se točka "naginje" prema kojem dijelu ruba.
# Traženi dio ruba (onaj koji ćemo sačuvati) je onaj koji zatvara manji kut s vektorom prema trenutnoj točci. (Nije moguće da oba dijela simetrale zatvaraju isti kut
# jer bi to značilo da neki rub ćelije prolazi kroz trenutnu točku, a to onda više nije Voronojeva ćelija
# Isto kao i sa postojećim rubom, moguže je da trenutna simetrala sjeće postojeći rub sa svojom krajnjom točkom
# U tom slučaju, cijela simetrala je točan rub ćelije
# U suprotnome, simetralu dijelimo na dva dijela
# Kako bi odredili koji dio trenutne simetrale spremamo za daljnju obradu, promatramo s koje strane POSTOJEĆEG RUBA, koji smo maloprije pronašli, se nalazi trenutna točka
# Strane dijelimo na "TRUE" i "FALSE" stranu
# Nakon što smo pronašli s koje strane postojećeg ruba se nalazi trenutna točka, pokušavamo pronaći s koje strane postojećeg ruba se nalazi bilo koja točka s lijevog i
# desnog dijela trenutne simetrale. Onaj dio koji se nalazi na istoj strani kao trenutna točka je točan dio trenutne simetrale
# Na kraju, kao trenutnu simetralu označavamo onaj dio trenutne simetrale koji je rub Voronojeve ćelije
# Još jedan edgecase koji se može javiti pri traženju rubova Voronojeve ćelije je ako su prve dvije simetrale koje pronađemo paralelne. U tom slučaju obje spremamo
# kao rubove ćelije.
# Kada smo završili sa traženjem pravilnih dijelova trenutne simetrale i trenutnog postojećeg ruba, uklanjamo rubove koje moramo
# To mogu biti stari postojeći rubovi koje smo upravo presjekli
# Na kraju ćemo ponovo morati pregledati sve postojeće rubove i po potrebi ukloniti neke koji "ne pašu"
# Kada uklonimo nepotrebne rubove, ostale spremamo kao točne rubove ćelije
# Kada pronađemo sve rubove ćelije, postoji vjerojatnost da nismo uklonili sve nepotrebne rubove. To su rubovi povezani sa presjećenim rubovima koje uklanjamo, ali ih nismo uklonili jer
# nismo znali da su povezani sa presječenim rubom
# Na kraju, uzimamo sve točke postojećih rubova i sortiramo ih po polarnom kutu kako bi mogli dobiti poredane točke poligona, odnosno ćelije

#Literatura: [Computational Geometry - An Introduction, str. 204]
def ukloni_iste_tocke(skup_tocaka):
    pom_lista = []
    for tocka1 in range(0, len(skup_tocaka)):
        duplikat = False
        for tocka2 in range(tocka1 + 1, len(skup_tocaka)):
            if (skup_tocaka[tocka1] == skup_tocaka[tocka2]):
                duplikat = True

        if (not duplikat):
            pom_lista.append(skup_tocaka[tocka1])

    return pom_lista

def uklanjanje_rubova(rubovi,za_ukloniti):
    for rub in za_ukloniti:
        for rub2 in rubovi:
            if (rub == rub2):
                rubovi.remove(rub2)
    return rubovi

def voronoi(tocke):

    tocke = list(set(tocke))

    if(len(tocke)<2):
        raise ValueError("Premalo točaka za izradu dijagrama!")

    if(len(tocke)==2):
        celije_dijagrama = []

        rub = Duzina(tocke[0],tocke[1]).simetrala()

        granicne_tocke = [Tocka(-1000000000,-1000000000),Tocka(1000000000,-1000000000),Tocka(1000000000,1000000000),Tocka(-1000000000,1000000000),]

        tocka_je_na_lijevoj_strani = Duzina(rub.B,rub.A).u_vektor().vektorski_produkt(Duzina(rub.A,tocke[0]).u_vektor())>0

        prvi_poligon = [tocka for tocka in granicne_tocke if (Duzina(rub.B,rub.A).u_vektor().vektorski_produkt(Duzina(rub.A,tocka).u_vektor())>0)==tocka_je_na_lijevoj_strani]
        prvi_poligon.append(rub.B)
        prvi_poligon.append(rub.A)
        prvi_poligon.sort(key=lambda t: (
            Duzina(tocke[0], tocke[0] + Tocka(1, 0)).u_vektor().kut_izmedu_vektora360(
            Duzina(tocke[0], t).u_vektor()), Duzina(tocke[0], t).u_vektor().duljina()))

        celije_dijagrama.append(VoronoiCelija(tocke[0],Poligon(prvi_poligon)))

        drugi_poligon = [tocka for tocka in granicne_tocke if (Duzina(rub.B,rub.A).u_vektor().vektorski_produkt(Duzina(rub.A,tocka).u_vektor())>0)!=tocka_je_na_lijevoj_strani]
        drugi_poligon.append(rub.B)
        drugi_poligon.append(rub.A)
        drugi_poligon.sort(key=lambda t: (
            Duzina(tocke[1], tocke[1] + Tocka(1, 0)).u_vektor().kut_izmedu_vektora360(
            Duzina(tocke[1], t).u_vektor()), Duzina(tocke[1], t).u_vektor().duljina()))

        celije_dijagrama.append(VoronoiCelija(tocke[1],Poligon(drugi_poligon)))

        return celije_dijagrama

    celije_dijagrama = []

    tocke_pom = [i for i in tocke]

    for trenutna_tocka in tocke_pom:
        tocke.sort(key=lambda tocka: trenutna_tocka.udaljenost_od(tocka))

        tocke.pop(0)

        rubovi = []

        pronadeno_bar_jedno_sjeciste = False

        for tocka in tocke:
            trenutna_duzina = Duzina(trenutna_tocka, tocka)
            trenutna_simetrala = trenutna_duzina.simetrala()

            if (len(rubovi) == 0):
                rubovi.append(trenutna_simetrala)

            else:
                za_ukloniti = []

                rubovi_pom = []

                postoji_sjeciste = False

                for postojeci_rub in rubovi:
                    sjeciste = trenutna_simetrala.sjeciste(postojeci_rub)

                    if (not (sjeciste.prazna())):
                        postoji_sjeciste = True
                        pronadeno_bar_jedno_sjeciste = True

                        if (postojeci_rub.A == sjeciste or postojeci_rub.B == sjeciste):
                            tocan_dio_postojeceg_ruba = postojeci_rub

                        else:
                            za_ukloniti.append(postojeci_rub)

                            lijeva_polovica_postojeceg_ruba = Duzina(postojeci_rub.A, sjeciste)
                            desna_polovica_postojeceg_ruba = Duzina(postojeci_rub.B, sjeciste)

                            tocan_dio_postojeceg_ruba = lijeva_polovica_postojeceg_ruba



                            vektor_do_trenutne_točke = Duzina(sjeciste, trenutna_tocka).u_vektor()

                            kut_između_lpolpostrub_i_vdtt = lijeva_polovica_postojeceg_ruba.u_vektor().kut_izmedu_vektora(
                                vektor_do_trenutne_točke)
                            kut_između_dpolpostrub_i_vdtt = desna_polovica_postojeceg_ruba.u_vektor().kut_izmedu_vektora(
                                vektor_do_trenutne_točke)


                            if (kut_između_lpolpostrub_i_vdtt < kut_između_dpolpostrub_i_vdtt):
                                tocan_dio_postojeceg_ruba = desna_polovica_postojeceg_ruba

                            rubovi_pom.append(tocan_dio_postojeceg_ruba)

                        if (trenutna_simetrala.A == sjeciste or trenutna_simetrala.B == sjeciste):
                            tocan_dio_trenutne_simetrale = trenutna_simetrala

                        else:
                            lijeva_polovica_trenutne_simetrale = Duzina(sjeciste, trenutna_simetrala.A)
                            desna_polovica_trenutna_simetrale = Duzina(sjeciste, trenutna_simetrala.B)

                            trenutna_tocka_je_na_lijevoj_strani = tocan_dio_postojeceg_ruba.u_vektor().vektorski_produkt(
                                vektor_do_trenutne_točke) > 0

                            lpoltrensim_pripada_poligonu = tocan_dio_postojeceg_ruba.u_vektor().vektorski_produkt(
                                lijeva_polovica_trenutne_simetrale.u_vektor()) > 0

                            if (lpoltrensim_pripada_poligonu == trenutna_tocka_je_na_lijevoj_strani):
                                tocan_dio_trenutne_simetrale = lijeva_polovica_trenutne_simetrale

                            else:
                                tocan_dio_trenutne_simetrale = desna_polovica_trenutna_simetrale

                        trenutna_simetrala = tocan_dio_trenutne_simetrale

                    elif (not pronadeno_bar_jedno_sjeciste):
                        rubovi_pom.append(trenutna_simetrala)

                rubovi = uklanjanje_rubova(rubovi,za_ukloniti) #break

                for rub in rubovi_pom:
                    rubovi.append(rub)

                if (postoji_sjeciste):
                    rubovi.append(trenutna_simetrala)

        for rub1 in rubovi:
            tocka_je_lijevo = rub1.u_vektor().vektorski_produkt(Duzina(rub1.B, trenutna_tocka).u_vektor()) > 0
            for rub2 in rubovi:
                if (not (rub2.A == rub1.A or rub2.A == rub1.B)):
                    tockaA_je_lijevo = rub1.u_vektor().vektorski_produkt(Duzina(rub1.B, rub2.A).u_vektor()) > 0
                    if (tockaA_je_lijevo != tocka_je_lijevo):
                        za_ukloniti.append(rub2)
                if (not (rub2.B == rub1.A or rub2.B == rub1.B)):
                    tockaB_je_lijevo = rub1.u_vektor().vektorski_produkt(Duzina(rub1.B, rub2.B).u_vektor()) > 0
                    if (tockaB_je_lijevo != tocka_je_lijevo):
                        za_ukloniti.append(rub2)

        rubovi = uklanjanje_rubova(rubovi,za_ukloniti)

        vrhovi = [t.A for t in rubovi]
        vrhovi += [t.B for t in rubovi if t.B not in vrhovi]

        vrhovi = ukloni_iste_tocke(vrhovi)

        vrhovi.sort(key=lambda t: (
        Duzina(trenutna_tocka, trenutna_tocka + Tocka(1, 0)).u_vektor().kut_izmedu_vektora360(
            Duzina(trenutna_tocka, t).u_vektor()), Duzina(trenutna_tocka, t).u_vektor().duljina()))

        voroni_celija = VoronoiCelija(trenutna_tocka, Poligon(vrhovi))

        celije_dijagrama.append(voroni_celija)

        tocke.insert(0, trenutna_tocka)

    return celije_dijagrama

def v_voronoi(tocke):
    celije_dijagrama = voronoi(tocke)

    for poligon in celije_dijagrama:
        poligon = poligon.Poligon.tocke
        plt.fill([t.x for t in poligon],[t.y for t in poligon],alpha=0.15)

    for poligon in celije_dijagrama:
        poligon = poligon.Poligon.u_duzine()
        for simetrala in poligon:
            plt.plot([simetrala.A.x,simetrala.B.x],[simetrala.A.y,simetrala.B.y],color="black")


    for tocka in tocke:
        plt.scatter(tocka.x,tocka.y,color="red",marker=".")

    xmin = abs(Poligon(tocke).min_x())
    xmax = abs(Poligon(tocke).max_x())
    ymin = abs(Poligon(tocke).min_y())
    ymax = abs(Poligon(tocke).max_y())

    x = xmin
    y = ymin

    if(x<xmax):
        x = xmax
    if(y<ymax):
        y = ymax

    x+=x*0.1
    y+=y*0.1
    plt.axis([-x,x,-y,y])
    plt.show()

def v_voronoi_test(broj_tocaka):

    tocke=[]

    while(len(tocke)<broj_tocaka):
        tocke = [Tocka(generiraj_broj(),generiraj_broj()) for i in range(broj_tocaka)]
        tocke = list(set(tocke))

    v_voronoi(tocke)



    # tocke = [Tocka(9,3),Tocka(-5,-5),Tocka(4, -3),Tocka(-6, 4),Tocka(1, 3),Tocka(1, 0),Tocka(-3, 9),Tocka(2, 6),Tocka(-4, 6),Tocka(2,-2),Tocka(7,0),]
    # #
    # tocke =[   Tocka(-2 , 9),Tocka(6 , 4),Tocka(4 , -8), ]
    # # #
    # tocke = [Tocka(-7 , -6),Tocka(-2 , -2),Tocka(-1 , 5)]
    # # #
    # tocke = [Tocka(3 , 1), Tocka(0 , 4), Tocka(0 , -2)]
    # # #
    # tocke = [ Tocka(-1 , 2), Tocka(0 , 3),Tocka(-2 , -1), Tocka(0 , -1),]
    # # #
    # tocke = [Tocka(1,0),Tocka(3,3),Tocka(0,-3),Tocka(0,-5),Tocka(4,-5),]
    # # #
    # tocke = [Tocka(5 , -8), Tocka(2 , -8), Tocka(1 , -4), Tocka(9 , 2), Tocka(-7 , -7), Tocka(-8 , 7),]
    # # #
    # tocke = [ Tocka(0 , 7),Tocka(-9 , -5),Tocka(-3 , 0), Tocka(1 , -8),Tocka(4 , 2),  Tocka(7 , 0), ]
    # # #
    # tocke = [Tocka(-2 , -3), Tocka(-9 , -1), Tocka(8 , -5), Tocka(-5 , 8), Tocka(-4 , 9)]
    # # #
    # tocke =[Tocka(9 , -7),Tocka(-7 , -4), Tocka(0 , 5), Tocka(9 , -4),  Tocka(6 , 6)]
    # # #
    # tocke = [Tocka(5 , -7), Tocka(1 , -7), Tocka(-1 , -8), Tocka(-3 , -9), Tocka(6 , 2)]
    # # #
    # tocke =  [ Tocka(5 , -3), Tocka(5 , 5),Tocka(5 , -8), Tocka(8 , 6), Tocka(-3 , 9)]
    # # #
    # tocke = [Tocka(0 , -2), Tocka(1 , -2), Tocka(0 , -4), Tocka(-1 , 0), Tocka(-3 , 0), Tocka(-4 , -2), Tocka(-4 , -1), Tocka(3 , 4), Tocka(-4 , 4)]
    # # #
    # tocke = [Tocka(-8 , 8), Tocka(-3 , -5), Tocka(7 , 2)]
    # # #
    # tocke = [Tocka(-4 , 0), Tocka(4 , 9), Tocka(2 , 4)]
    # # #
    # tocke = [Tocka(9 , 0), Tocka(9 , 2), Tocka(-5 , 0)]
    # # #
    # tocke = [Tocka(-1 , -7), Tocka(2 , 0), Tocka(7 , 4)]
    # # #
    # tocke = [Tocka(8 , -5), Tocka(-5 , -6), Tocka(-4 , 3)]
    # # #
    # tocke = [Tocka(4 , 8), Tocka(-8 , -4), Tocka(5 , 2)]
    # # #
    # tocke = [Tocka(6 , 4), Tocka(4 , -8), Tocka(-2 , 9)]
    # # #
    # tocke = [Tocka(-4 , 4), Tocka(6 , -3), Tocka(-8 , 6)]
    # # #
    # tocke = [Tocka(3 , 1), Tocka(0 , 4), Tocka(0 , -2)]
    # # #
    # tocke = [Tocka(-1 , 2), Tocka(0 , 3), Tocka(-2 , -1), Tocka(0 , -1)]
    # # #
    # tocke = [ Tocka(0,1), Tocka(-2,0), Tocka(0,-3), Tocka(3,4)]
    # # #
    # tocke = [ Tocka(1,0), Tocka(3,3), Tocka(0,-3), Tocka(0,-5), Tocka(4,-5),]
    # # #
    # tocke = [Tocka(-3.1683908934753617 , -4.653706072281693), Tocka(-4.355690592880592 , 0.6006362024813825), Tocka(-0.9136761660038246 , 4.3713870698911705), Tocka(1.9514248983439302 , 3.7028994697220696), Tocka(1.7354732689213108 , 4.111435949275574), Tocka(5.004579181639201 , 3.56763219487857)]
    # # #
    # tocke = [Tocka(-2 , -3), Tocka(-9 , -1), Tocka(8 , -5), Tocka(-5 , 8), Tocka(-4 , 9)]
    # # #
    # tocke = [Tocka(-7 , 5), Tocka(-2 , 6), Tocka(-6 , -1), Tocka(-7 , -2), Tocka(0 , 8), Tocka(3 , 3), Tocka(-9 , -9), Tocka(3 , -7)]
    # # #
    # tocke = [Tocka(-7 , -4), Tocka(0 , 5), Tocka(9 , -4), Tocka(9 , -7), Tocka(6 , 6)]
    # # #
    # tocke = [Tocka(-1 , -2),Tocka(2 , -2), Tocka(1 , -1),  Tocka(0 , -1)]
    # # #
    # tocke = [Tocka(1 , 1), Tocka(2 , 0), Tocka(1 , -1), Tocka(2 , -1)]
    # # #
    # tocke = [Tocka(-1,0),Tocka(0,0),Tocka(-2,2),Tocka(-2,1),Tocka(0,2),Tocka(0,1),Tocka(-1,1),Tocka(-1,2),Tocka(-2,0),]
    # # #
    # tocke = [Tocka(2 , 2),  Tocka(1 , 1), Tocka(2 , 1),Tocka(1 , 3),]
    # # #
    # tocke = [ Tocka(-3 , 0),Tocka(-1 , 0), Tocka (-4 , -2), Tocka(-4 , -1),Tocka(-4 , 4),Tocka(0 , -2),]
    # # #
    # tocke = [  Tocka(-1 , 0),Tocka(0 , 0), Tocka(1 , 0),  Tocka(1 , 3),]
    # # #
    # tocke = [Tocka(0,0),Tocka(1,0),Tocka(0,1),Tocka(1,1)]
    # # #
    # tocke=[ Tocka(2 , -4), Tocka(-2 , -1), Tocka(3 , 1), Tocka(1 , -4), Tocka(5 , 0), Tocka(0 , -7),  Tocka(8 , -2), Tocka(8 , -5),] -- krivo vraća vjv zbog preciznosti
    # # #
    # tocke=[  Tocka(-2 , -1),Tocka(1 , -4),Tocka(5 , 0), Tocka(0 , -7),  Tocka(7 , 9), Tocka(8 , -2),Tocka(8 , -5), Tocka(2 , -4),] -- krivo vraća vjv zbog preciznosti
    # #
    # tocke =  [Tocka(-3 , -1), Tocka(-1 , 0), Tocka(-5 , -4), Tocka(-1 , -3),  Tocka(1 , 5), Tocka(-2 , 0),]
    #
    # tocke = [Tocka(1 , -3), Tocka(0 , -3), Tocka(-2 , -2), Tocka(-2 , -4),Tocka (6 , -2),Tocka (2 , -8),Tocka (-3 , -7),Tocka (7 , -5),Tocka (-4 , 1),Tocka (8 , -2),Tocka (9 , -2), Tocka(9 , 0), Tocka(0 , 8), Tocka(5 , 9), Tocka(-7 , 7)]
    #
    # tocke =  [ Tocka(3 , -4), Tocka(5 , -2),Tocka (2 , -8), Tocka(7 , -8), Tocka(-3 , -2),Tocka (-1 , 1), Tocka(0 , 3), Tocka(3 , 4), Tocka(-5 , -7), Tocka(-4 , 1), Tocka(-3 , 5), Tocka(8 , 6), Tocka(-8 , -9),Tocka (-7 , 3), Tocka(-2 , 8)] -- krivo vraća vjv zbog preciznosti


