"""Sadrži funkcije za izradu Voronojevog dijagrama
"""
from konveksnaljuska import *

# Prvo uklanjamo duplikatne točke u danom skupu.  Ako su zadane samo
# dvije točke, koristimo poseban algoritam koji stvara samo jednu
# simetralu i dijeli prostor na dva četverokuta:
#
#    Prvo stvaramo simetralu dužine koju čine dane dvije točke.  Nakon
#    toga zadajemo 4 točke koje su proizvoljno daleko od središta
#    koordinatnog sustava.  Određujemo na kojoj strani se nalazi jedna
#    od točaka zadanih u skupu točaka.  Prvi poligon (buduću ćeliju
#    dijagrama) će činiti točke simetrale i sve granične točke koje se
#    nalaze na istoj strani kao odabrana točka simetrale.  Kako bismo
#    dobili poligon, sortiramo točke na temelju polarnog kuta.  Postupak
#    za drugi poligon je identičan, osim što u njega spremamo granične
#    točke sa suprotne strane.
#
# Cilj je za svaku točku pronaći sve simetrale koje čine njihove dužine
# sa svim ostalim točkama u skupu. Te simetrale i njihova sjecišta činiti
# će poligon, odnosno Voronojevu ćeliju.  Prvo sortiramo sve točke po
# udaljenosti od trenutne točke koju promatramo. To radimo kako bi što
# prije pronašli poligon/ćeliju.  Za svaku točku u skupu pronalazimo
# simetralu dužine koja ona čini s trenutnom točkom.  Ukoliko smo našli
# simetralu s prvom točkom, odmah ju spremamo kao jedan rub poligona.  U
# suprotnome, prvo tražimo sjecište između postojećih rubova i trenutne
# simetrale koju promatramo.
#
# Ako postoji sjecište, znači da trenutna simetrala dijeli postojeći rub
# na dva dijela kao što i postojeći rub dijeli trenutnu simetralu na dva
# dijela.  Iznimno, može se desiti da se trenutna simetrala i postojeći
# rub sjeku u nekoj krajnjoj točci.  Ako trenutna simetrala sjeće
# postojeći rub u krajnjoj točci, tada će postojeći rub ostati u listi
# točnih rubova Voronojeve ćelije.
#
# U suprotnome, uklanjamo cijeli postojeći rub (jer neće cijeli rub
# činiti stranicu ćelije, već samo jedan od njena dva dijela).  Rub se
# dijeli na dio od točke A do sjecišta i od sjecišta do točke B.  Za
# početak predstavljamo da je "lijeva polovica" točna polovica koja
# će činiti rub Voronojeve ćelije (zapravo nema lijeve i desne polovice,
# samo se tako nazivaju).  Kako bi pronašli koja polovica je "točna"
# (čini rub Voronojeve ćelije), promatramo koliki kut zatvaraju vektori
# koje čine dijelovi ruba s vektorom od sjecišta do trenutne točke.  Što
# je kut između vektora manji, to je trenutna točka "bliže" određenom
# dijelu ruba.  Zapravo gledamo koliko se točka "naginje" prema kojem
# dijelu ruba.  Traženi dio ruba (onaj koji ćemo sačuvati) je onaj koji
# zatvara manji kut s vektorom prema trenutnoj točci. (Nije moguće da oba
# dijela simetrale zatvaraju isti kut jer bi to značilo da neki rub ćelije
# prolazi kroz trenutnu točku, a to onda više nije Voronojeva ćelija).
# Isto kao i sa postojećim rubom, moguže je da trenutna simetrala sjeće
# postojeći rub sa svojom krajnjom točkom.  U tom slučaju, cijela simetrala
# je točan rub ćelije.  U suprotnome, simetralu dijelimo na dva dijela.
# Kako bi odredili koji dio trenutne simetrale spremamo za daljnju obradu,
# promatramo s koje strane POSTOJEĆEG RUBA, koji smo maloprije pronašli, se
# nalazi trenutna točka.  Strane dijelimo na "TRUE" i "FALSE" stranu.  Nakon
# što smo pronašli s koje strane postojećeg ruba se nalazi trenutna točka,
# pokušavamo pronaći s koje strane postojećeg ruba se nalazi bilo koja točka
# s lijevog i desnog dijela trenutne simetrale. Onaj dio koji se nalazi na
# istoj strani kao trenutna točka je točan dio trenutne simetrale
# Na kraju, kao trenutnu simetralu označavamo onaj dio trenutne simetrale
# koji je rub Voronojeve ćelije.  Još jedan edgecase koji se može javiti
# pri traženju rubova Voronojeve ćelije je ako su prve dvije simetrale koje
# pronađemo paralelne. U tom slučaju obje spremamo kao rubove ćelije. Kada
# smo završili sa traženjem pravilnih dijelova trenutne simetrale i
# trenutnog postojećeg ruba, uklanjamo rubove koje moramo.  To mogu biti
# stari postojeći rubovi koje smo upravo presjekli.  Na kraju ćemo ponovo
# morati pregledati sve postojeće rubove i po potrebi ukloniti neke koji
# "ne pašu".  Kada uklonimo nepotrebne rubove, ostale spremamo kao točne
# rubove ćelije.  Kada pronađemo sve rubove ćelije, postoji vjerojatnost
# da nismo uklonili sve nepotrebne rubove. To su rubovi povezani sa
# presjećenim rubovima koje uklanjamo, ali ih nismo uklonili jer nismo
# znali da su povezani sa presječenim rubom.  Na kraju, uzimamo sve
# točke postojećih rubova i sortiramo ih po polarnom kutu kako bi mogli
# dobiti poredane točke poligona, odnosno ćelije.
# Literatura: [Computational Geometry - An Introduction, str. 204]


def ukloni_iste_tocke(skup_tocaka):
    """

    """
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
    """

    """
    for rub in za_ukloniti:
        for rub2 in rubovi:
            if (rub == rub2):
                rubovi.remove(rub2)
    return rubovi


def voronoi_za_dvije_tocke(prva_tocka,druga_tocka):
    """

    """
    celije_dijagrama = []
    rub = Duzina(prva_tocka, druga_tocka).simetrala()

    daleka_tocka = 1000000000

    granicne_tocke = [Tocka(-daleka_tocka, -daleka_tocka),
                      Tocka(daleka_tocka, -daleka_tocka),
                      Tocka(daleka_tocka, daleka_tocka),
                      Tocka(-daleka_tocka, daleka_tocka),
                      ]

    tocka_je_na_lijevoj_strani = prva_tocka.lijevo_od(rub)

    vrhovi_prvog_poligona = []
    vrhovi_drugog_poligona = []

    for tocka in granicne_tocke:
        if(tocka.lijevo_od(rub)==tocka_je_na_lijevoj_strani):
            vrhovi_prvog_poligona.append(tocka)
        else:
            vrhovi_drugog_poligona.append(tocka)

    vrhovi_prvog_poligona.append(rub.B)
    vrhovi_prvog_poligona.append(rub.A)
    vrhovi_drugog_poligona.append(rub.B)
    vrhovi_drugog_poligona.append(rub.A)

    vrhovi_prvog_poligona.sort(
        key=lambda vrh: (prva_tocka.polarni_kut(vrh),
                         Duzina(prva_tocka, vrh).u_vektor().duljina()))

    vrhovi_drugog_poligona.sort(
        key=lambda vrh: (druga_tocka.polarni_kut(vrh),
                         Duzina(druga_tocka, vrh).u_vektor().duljina()))

    prvi_poligon = Poligon(vrhovi_prvog_poligona)
    drugi_poligon = Poligon(vrhovi_drugog_poligona)
    celije_dijagrama.append(VoronoiCelija(prva_tocka, prvi_poligon))
    celije_dijagrama.append(VoronoiCelija(druga_tocka, drugi_poligon))

    return celije_dijagrama

def voronoi(tocke):
    """

    """

    tocke = list(set(tocke))

    if(len(tocke)<2):
        raise ValueError("Premalo točaka za izradu dijagrama!")

    if(len(tocke)==2):
       return voronoi_za_dvije_tocke(tocke[0],tocke[1])

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
#123456789012345678901234567890123456789012345678901234567890123456789012345678
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

                            trenutna_tocka_je_na_lijevoj_strani = trenutna_tocka.lijevo_od(tocan_dio_postojeceg_ruba)

                            lpoltrensim_pripada_poligonu = trenutna_simetrala.A.lijevo_od(tocan_dio_postojeceg_ruba)

                            if (lpoltrensim_pripada_poligonu == trenutna_tocka_je_na_lijevoj_strani):
                                tocan_dio_trenutne_simetrale = lijeva_polovica_trenutne_simetrale

                            else:
                                tocan_dio_trenutne_simetrale = desna_polovica_trenutna_simetrale
#123456789012345678901234567890123456789012345678901234567890123456789012345678
                        trenutna_simetrala = tocan_dio_trenutne_simetrale

                    elif (not pronadeno_bar_jedno_sjeciste):
                        rubovi_pom.append(trenutna_simetrala)

                rubovi = uklanjanje_rubova(rubovi,za_ukloniti)

                for rub in rubovi_pom:
                    rubovi.append(rub)

                if (postoji_sjeciste):
                    rubovi.append(trenutna_simetrala)

        for rub_1 in rubovi:
            tocka_je_lijevo = trenutna_tocka.lijevo_od(rub_1)
            for rub_2 in rubovi:
                if (not (rub_2.A == rub_1.A or rub_2.A == rub_1.B)):
                    tockaA_je_lijevo = rub_2.A.lijevo_od(rub_1)
                    if (tockaA_je_lijevo != tocka_je_lijevo):
                        za_ukloniti.append(rub_2)
                if (not (rub_2.B == rub_1.A or rub_2.B == rub_1.B)):
                    tockaB_je_lijevo =rub_2.B.lijevo_od(rub_1)
                    if (tockaB_je_lijevo != tocka_je_lijevo):
                        za_ukloniti.append(rub_2)

        rubovi = uklanjanje_rubova(rubovi,za_ukloniti)

        vrhovi = [t.A for t in rubovi]
        vrhovi += [t.B for t in rubovi if t.B not in vrhovi]

        vrhovi = ukloni_iste_tocke(vrhovi)

        vrhovi.sort(
            key=lambda tocka:
            (trenutna_tocka.polarni_kut(tocka),
             Duzina(trenutna_tocka, tocka).u_vektor().duljina()))

        voroni_celija = VoronoiCelija(trenutna_tocka, Poligon(vrhovi))

        celije_dijagrama.append(voroni_celija)

        tocke.insert(0, trenutna_tocka)

    return celije_dijagrama