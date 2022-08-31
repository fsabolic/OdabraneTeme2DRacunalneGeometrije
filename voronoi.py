"""Sadrži funkcije za izradu Voronojevog dijagrama
"""
from klase import *
from iznimke import PremaloTocakaError


def ukloni_iste_tocke(skup_tocaka):
    """Uklanja duplikate iz skupa točaka."""
    pom_lista = []
    for tocka1 in range(0, len(skup_tocaka)):
        duplikat = False
        for tocka2 in range(tocka1 + 1, len(skup_tocaka)):
            if skup_tocaka[tocka1] == skup_tocaka[tocka2]:
                duplikat = True

        if not duplikat:
            pom_lista.append(skup_tocaka[tocka1])

    return pom_lista


def uklanjanje_rubova(rubovi, za_ukloniti):
    """Uklanja rubove koji se nalaze u oba zadana skupa.

    Parametri
    ---------
    rubovi: lista Duzina

    za_ukloniti: lista Duzina


    Vraća
    -----
    rubovi: lista Duzina
    """
    for rub in za_ukloniti:
        for rub2 in rubovi:
            if rub == rub2:
                rubovi.remove(rub2)
    return rubovi


def voronoi_za_dvije_tocke(prva_tocka, druga_tocka):
    """Izrađuje Voronojev dijagram za dvije točke.

    Parametri
    ---------
    prva_tocka,druga_tocka: Tocka

    Vraća
    -----
    celije_dijagrama: lista VoronoiCelija

    """
    celije_dijagrama = []
    rub = Duzina(prva_tocka, druga_tocka).simetrala()

    daleka_tocka = 100000000

    granicne_tocke = [Tocka(-daleka_tocka, -daleka_tocka),
                      Tocka(daleka_tocka, -daleka_tocka),
                      Tocka(daleka_tocka, daleka_tocka),
                      Tocka(-daleka_tocka, daleka_tocka),
                      ]

    tocka_je_na_lijevoj_strani = prva_tocka.lijevo_od(rub)

    vrhovi_prvog_poligona = []
    vrhovi_drugog_poligona = []

    for tocka in granicne_tocke:
        if tocka.lijevo_od(rub) == tocka_je_na_lijevoj_strani:
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
    """Izrađuje Voronojev dijagram za skup točaka.

    Parametri
    ---------
    tocke: lista Tocaka

    Vraća
    -----
    celije_dijagrama: lista VoronoiCelija

    Iznimke
    -------
    PremaloTocakaError
        U slučaju da je dana samo jedna točka nije moguće odrediti Voronojev dijagram.
    """

    tocke = list(set(tocke))

    if len(tocke) < 2:
        raise PremaloTocakaError("Premalo točaka za izradu dijagrama!")

    if len(tocke) == 2:
        return voronoi_za_dvije_tocke(tocke[0], tocke[1])

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

            if len(rubovi) == 0:
                rubovi.append(trenutna_simetrala)

            else:
                za_ukloniti = []

                rubovi_pom = []

                postoji_sjeciste = False

                for postojeci_rub in rubovi:
                    sjeciste = trenutna_simetrala.sjeciste(postojeci_rub)

                    if not sjeciste.prazna():
                        postoji_sjeciste = True
                        pronadeno_bar_jedno_sjeciste = True
                        if (postojeci_rub.A ==
                                sjeciste or postojeci_rub.B == sjeciste):
                            tocan_dio_postojeceg_ruba = postojeci_rub

                        else:
                            za_ukloniti.append(postojeci_rub)

                            lijeva_polovica_postojeceg_ruba = Duzina(
                                postojeci_rub.A, sjeciste)
                            desna_polovica_postojeceg_ruba = Duzina(
                                postojeci_rub.B, sjeciste)

                            tocan_dio_postojeceg_ruba = \
                                lijeva_polovica_postojeceg_ruba

                            vektor_do_trenutne_točke = Duzina(
                                sjeciste, trenutna_tocka).u_vektor()

                            kut_između_lpolpostrub_i_vdtt = \
                                lijeva_polovica_postojeceg_ruba.u_vektor()\
                                    .kut_izmedu_vektora(vektor_do_trenutne_točke)
                            kut_između_dpolpostrub_i_vdtt = \
                                desna_polovica_postojeceg_ruba.u_vektor()\
                                    .kut_izmedu_vektora(vektor_do_trenutne_točke)

                            if (kut_između_lpolpostrub_i_vdtt <
                                    kut_između_dpolpostrub_i_vdtt):
                                tocan_dio_postojeceg_ruba = \
                                    desna_polovica_postojeceg_ruba

                            rubovi_pom.append(tocan_dio_postojeceg_ruba)

                        if (trenutna_simetrala.A ==
                                sjeciste or trenutna_simetrala.B == sjeciste):
                            tocan_dio_trenutne_simetrale = trenutna_simetrala

                        else:
                            lijeva_polovica_trenutne_simetrale = Duzina(
                                sjeciste, trenutna_simetrala.A)
                            desna_polovica_trenutna_simetrale = Duzina(
                                sjeciste, trenutna_simetrala.B)

                            trenutna_tocka_je_na_lijevoj_strani = \
                                trenutna_tocka.lijevo_od(
                                    tocan_dio_postojeceg_ruba)

                            lpoltrensim_pripada_poligonu = \
                                trenutna_simetrala.A.lijevo_od(
                                    tocan_dio_postojeceg_ruba)

                            if (lpoltrensim_pripada_poligonu ==
                                    trenutna_tocka_je_na_lijevoj_strani):
                                tocan_dio_trenutne_simetrale = \
                                    lijeva_polovica_trenutne_simetrale

                            else:
                                tocan_dio_trenutne_simetrale = \
                                    desna_polovica_trenutna_simetrale
                        trenutna_simetrala = tocan_dio_trenutne_simetrale

                    elif not pronadeno_bar_jedno_sjeciste:
                        rubovi_pom.append(trenutna_simetrala)

                rubovi = uklanjanje_rubova(rubovi, za_ukloniti)

                for rub in rubovi_pom:
                    rubovi.append(rub)

                if postoji_sjeciste:
                    rubovi.append(trenutna_simetrala)

        for rub_1 in rubovi:
            tocka_je_lijevo = trenutna_tocka.lijevo_od(rub_1)
            for rub_2 in rubovi:
                if not (rub_2.A == rub_1.A or rub_2.A == rub_1.B):
                    tockaA_je_lijevo = rub_2.A.lijevo_od(rub_1)
                    if tockaA_je_lijevo != tocka_je_lijevo:
                        za_ukloniti.append(rub_2)
                if not (rub_2.B == rub_1.A or rub_2.B == rub_1.B):
                    tockaB_je_lijevo = rub_2.B.lijevo_od(rub_1)
                    if tockaB_je_lijevo != tocka_je_lijevo:
                        za_ukloniti.append(rub_2)

        rubovi = uklanjanje_rubova(rubovi, za_ukloniti)

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
