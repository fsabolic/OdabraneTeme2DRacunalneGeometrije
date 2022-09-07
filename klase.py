"""Sadrži klase i funkcije za rad sa osnovnim 2D geometrijskim objektima.

Modul sadrži klase za rad s točkama, dužinama, poligonima i vektorima. Osim
toga, sadrži klasu za pohranjihvanje podataka iz Voronojeveg dijagrama i
nekoliko pomoćnih klasa koje nemaju nisu namijenjene za korištenje izvan
modula.

Atributi
--------
EPSILON: float
    Koristi se za preciznost pri uspordbama

"""
import math
from iznimke import IsteKrajnjeTockeError

EPSILON = 0.000001


class Tocka:
    """Prikaz 2D točke u koordinatnom sustavu.

    Parametri
    ---------
    x: float
        Apscisa točke.
    y: float
        Ordinata točke.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, tocka):
        """Provjerava jesu li dvije točke jednake.

        Provjerava jesu li dvije točke jednake s dozvoljenom preciznošću od EPSILON.

        Parametri
        ---------
        tocka: Tocka

        Vraća
        -----
        :bool
        """
        if (self.x is None or self.y is None
                or tocka.x is None or tocka.y is None):
            return self.x == tocka.x and self.y == tocka.y

        return abs(
            self.x -
            tocka.x) < EPSILON and abs(
            self.y -
            tocka.y) < EPSILON

    def __hash__(self):
        return hash(self.x + self.y)

    def __add__(self, tocka):
        """Zbraja dva objekta klase Tocka.

        Parametri
        ---------
        tocka: Tocka

        Vraća
        -----
        :Tocka
            Točka čije koordinate su zbroj apscisa i ordinata danih točaka.
        """
        return Tocka(self.x + tocka.x, self.y + tocka.y)

    def __sub__(self, tocka):
        """Oduzima dva objekta klase Tocka

        """
        return Tocka(self.x - tocka.x, self.y - tocka.y)

    def __repr__(self):
        """Prikaz objekta klase Tocka"""
        return "(%s , %s)" % (self.x, self.y)

    def __str__(self):
        """Prikaz objekta klase Tocka"""
        return "(%s , %s)" % (self.x, self.y)

    def prazna(self):
        """Provjerava jesu li atributi dane točke oba None."""
        return self == Tocka(None, None)

    def mnozenje_skalarom(self, skalar):
        """Vraća danu točku čije koordinate su pomnožene skalarom.

        Parametri
        ---------
        skalar: float
            Realni broj s kojim će se množiti koordinate točke.

        Vraća
        -----
        :Tocka

        """
        return Tocka(self.x * skalar, self.y * skalar)

    def lijevo_od(self, duzina):
        """Provjerava je li dana točka s lijeve strane vektora predstavljenog dužinom.

        Parametri
        ---------
        duzina: Duzina

        Vraća
        -----
        :bool

        Napomena
        --------
        Kako dužina nema smjer, dužina se prvo pretvara u vektor
        """
        vektor = duzina.u_vektor()
        tocka = Duzina(duzina.B, self).u_vektor()
        return vektor.vektorski_produkt(tocka) > 0

    def pripada_duzini(self, duzina):
        """Provjerava nalazi li se točka na danoj dužini."""
        if self in (duzina.A, duzina.B):
            return True

        v_1 = duzina.u_vektor()
        v_2 = Duzina(duzina.A, self).u_vektor()
        if not v_1 // v_2:
            return False

        skalarni_produkt = v_2.skalarni_produkt(v_1)
        if skalarni_produkt < 0:
            return False

        kvadratna_duljina = v_1.i**2 + v_1.j**2
        return not skalarni_produkt > kvadratna_duljina

    def pripada_poligonu(self, poligon):
        """Provjerava nalazi li se točka unutar nekog poligona.

        Algoritam se izvršava pomoću Ray Casting algoritma.

        Parametri
        ---------
        poligon:Poligon

        Vraća
        -----
        :int
            Vraća 0 (točka je na rubu poligona), -1 (točka je izvan poligona) ili
            1 (točka je unutar poligona).

        """
        najdesnija_tocka_plus = Tocka(poligon.max_x() + 1, self.y)
        if najdesnija_tocka_plus == self:
            return -1

        duzina_za_presjek = Duzina(self, najdesnija_tocka_plus)
        rubovi_poligona = poligon.rubovi()
        sjecista = 0
        for rub in rubovi_poligona:
            if self.pripada_duzini(rub):
                return 0
            if not rub.u_vektor() // duzina_za_presjek.u_vektor():
                sjec = duzina_za_presjek.sjeciste(rub)
                if not sjec.prazna():
                    if (sjec in (rub.A, rub.B)
                            and sjec.y == rub.manja_oridnata()
                            or sjec not in (rub.A, rub.B)):
                        sjecista += 1

        return 1 + (sjecista % 2 == 0) * -2

    def pripada_poligonu_wn(self, poligon):
        """Provjerava nalazi li se točka unutar nekog poligona.

        Algoritam se izvršava pomoću Winding Number algoritma.

        Parametri
        ---------
        poligon:Poligon

        Vraća
        -----
        :int
            Vraća 0 (točka je na rubu poligona), -1 (točka je izvan poligona) ili
            1 (točka je unutar poligona).

        """
        vrhovi_poligona = poligon.vrhovi
        br_tocaka = poligon.broj_vrhova()

        zbroj_kuteva = 0
        for i in range(0, br_tocaka):
            tocka_n = vrhovi_poligona[i]
            tocka_n_1 = vrhovi_poligona[(i + 1) % br_tocaka]
            rub_poligona = Duzina(tocka_n, tocka_n_1)

            if self.pripada_duzini(rub_poligona):
                return 0

            vektor_tocka_n = Duzina(self, tocka_n).u_vektor()
            vektor_tocka_n_1 = Duzina(self, tocka_n_1).u_vektor()

            vektor_tocka_yos = Duzina(self, self + Tocka(0, 1)).u_vektor()

            kut = (vektor_tocka_n_1.kut_izmedu_vektora360(vektor_tocka_yos)
                   - vektor_tocka_n.kut_izmedu_vektora360(vektor_tocka_yos))

            if kut > math.pi:
                kut -= 2 * math.pi

            if kut < -math.pi:
                kut += 2 * math.pi

            zbroj_kuteva += kut

        if abs(zbroj_kuteva) - EPSILON < 0 and abs(zbroj_kuteva) + EPSILON > 0:
            unutra = -1
        else:
            unutra = 1

        return unutra

    def udaljenost_od(self, tocka):
        """Vraća udaljenost između dviju točaka."""
        return math.sqrt((self.x - tocka.x) ** 2 + (self.y - tocka.y) ** 2)

    def polarni_kut(self, tocka):
        """Vraća "polarni kut" pomoću dvije točke.

        Vraća polarni kut između vektora koji počinje od dane točke i
        paralelan je s x-osi i translatiranog pozicijskog vektora druge
        dane točke.

        Parametri
        ---------
        tocka: Tocka

        Vraća
        -----
        :float

        """
        y_os_vektor = Duzina(self,
                             self + Tocka(1, 0)).u_vektor()
        pozicijski_vektor = Duzina(self,
                                   tocka).u_vektor()

        return y_os_vektor.kut_izmedu_vektora360(pozicijski_vektor)


class Duzina:
    """Prikaz 2D dužine u koordinatnom sustavu.

    Parametri
    ---------
    A,B: Tocka
        Krajnje točke dužine.

    Iznimke
    -------
    IstekKrajnjeTockeError
        Javlja se kada je dužina inicijalizirana s dvije krajnje točke koje
        imaju jednake vrijednosti x i y koordinata.
    """

    def __init__(self, A, B):
        if A != B:
            self.A = A
            self.B = B
        else:
            raise IsteKrajnjeTockeError()

    def __hash__(self):
        return hash(self.A + self.B)

    def __eq__(self, other):
        """Provjerava jesu li krajnje točke dviju dužina jednake."""
        return ((self.A == other.A and self.B == other.B)
                or (self.B == other.A and self.A == other.B))

    def __repr__(self):
        """Prikaz objekta klase Duzina"""
        return "(%s , %s)" % (self.A, self.B)

    def __str__(self):
        """Prikaz objekta klase Duzina"""
        return "(%s , %s)" % (self.A, self.B)

    def u_vektor(self):
        """Pretvara objekt klase Duzina u objekt klase Vektor"""
        return Vektor((self.B - self.A).x, (self.B - self.A).y)

    def presjek(self, duzina):
        """Provjerava sijeku li se dvije dužine.

        Parametri
        ---------
        duzina: Duzina

        Vraća
        -----
        :bool
        """
        vektor_self = self.u_vektor()
        vektor_other = duzina.u_vektor()
        if vektor_self // vektor_other:
            return (duzina.A.pripada_duzini(self)
                    or duzina.B.pripada_duzini(self)
                    or self.A.pripada_duzini(duzina)
                    or self.B.pripada_duzini(duzina))

        t = ((self.A.x * (duzina.B.y - duzina.A.y)
             + duzina.A.x * (self.A.y - duzina.B.y)
             + duzina.B.x * (duzina.A.y - self.A.y))
             / (vektor_other.vektorski_produkt(vektor_self)))

        s = ((self.A.x * (duzina.A.y - self.B.y)
             + self.B.x * (self.A.y - duzina.A.y)
             + duzina.A.x * (self.B.y - self.A.y))
             / (vektor_self.vektorski_produkt(vektor_other)))

        if 0 <= t <= 1 and 0 <= s <= 1:
            return True

        return False

    def sjeciste(self, duzina):
        """Vraća sjecište dviju dužina.

        Parametri
        ---------
        duzina: Duzina

        Vraća
        -----
        :Tocka
            Ukoliko sjecište ne postoji vraća se prazna točka, a u suprotnom vraća
            se točka u kojoj se sijeku dviju dužine.
        """
        vektor_self = self.u_vektor()
        vektor_other = duzina.u_vektor()
        if vektor_self // vektor_other:
            if duzina.A.pripada_duzini(self):
                return duzina.A
            elif duzina.B.pripada_duzini(self):
                return duzina.B
            elif self.A.pripada_duzini(duzina):
                return self.A
            elif self.B.pripada_duzini(duzina):
                return self.B
            else:
                return Tocka(None, None)

        t = ((self.A.x * (duzina.B.y - duzina.A.y)
              + duzina.A.x * (self.A.y - duzina.B.y)
              + duzina.B.x * (duzina.A.y - self.A.y))
             / (vektor_other.vektorski_produkt(vektor_self)))

        s = ((self.A.x * (duzina.A.y - self.B.y)
              + self.B.x * (self.A.y - duzina.A.y)
              + duzina.A.x * (self.B.y - self.A.y))
             / (vektor_self.vektorski_produkt(vektor_other)))

        if 0 <= t <= 1 and 0 <= s <= 1:
            return self.A + (self.B - self.A).mnozenje_skalarom(t)

        return Tocka(None, None)

    def manja_oridnata(self):
        """Vraća manju ordinatu dviju krajnjih točaka."""
        pom = self.A.y
        if pom > self.B.y:
            pom = self.B.y
        return pom

    def veca_ordinata(self):
        """Vraća veću ordinatu dviju krajnjih točaka."""
        pom = self.A.y
        if pom < self.B.y:
            pom = self.B.y
        return pom

    def simetrala(self):
        """Vraća simetralu dane dužine."""
        tocka_A = self.A
        tocka_B = self.B

        daleka_tocka = 100000000

        srediste = Tocka((tocka_A.x + tocka_B.x) / 2,
                         (tocka_A.y + tocka_B.y) / 2)

        if tocka_A.y == tocka_B.y:
            tocka_sim_A = Tocka(srediste.x, daleka_tocka)
            tocka_sim_B = Tocka(srediste.x, -daleka_tocka)

        elif tocka_A.x == tocka_B.x:
            koeficijent = 0
            tocka_sim_A = \
                Tocka(daleka_tocka,
                      srediste.y + koeficijent * (daleka_tocka - srediste.x))
            tocka_sim_B = \
                Tocka(-daleka_tocka,
                      srediste.y + koeficijent * (-daleka_tocka - srediste.x))

        else:
            koeficijent = -1 / ((tocka_B.y - tocka_A.y) /
                                (tocka_B.x - tocka_A.x))
            tocka_sim_A = \
                Tocka(daleka_tocka,
                      koeficijent * (daleka_tocka - srediste.x) + srediste.y)
            tocka_sim_B =\
                Tocka(-daleka_tocka,
                      koeficijent * (-daleka_tocka - srediste.x) + srediste.y)

        return Duzina(tocka_sim_A, tocka_sim_B)


class Vektor:
    """Prikaz vektora u 2D koordinatnom sustavu.

    Parametri
    ---------
    i,j: float
        Koeficijenti jediničnih vektor koji čine dani vektor.

    """

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __add__(self, vektor):
        """Vraća zbroj dvaju vektora."""
        return Vektor(self.i + vektor.i, self.j + vektor.j)

    def __neg__(self):
        """Vraća vektor pomnožen s negativnim skalarom."""
        return Vektor(-self.i, -self.j)

    def __floordiv__(self, vektor):
        """Provjerava jesu li dva vektora paralelna."""
        return self.vektorski_produkt(vektor) == 0

    def __repr__(self):
        """Prikaz objekta klase Vektor"""
        return "(%s , %s)" % (self.i, self.j)

    def __str__(self):
        """Prikaz objekta klase Vektor"""
        return "(%s , %s)" % (self.i, self.j)

    def duljina(self):
        """Vraća duljinu vektora."""
        return (self.i**2 + self.j**2)**(1 / 2)

    def skalarni_produkt(self, vektor):
        """Vraća skalarni produkt dvaju vektora."""
        return self.i * vektor.i + self.j * vektor.j

    def vektorski_produkt(self, vektor):
        """Vraća vektorski produkt dvaju vektora."""
        return (self.i) * (vektor.j) - (vektor.i) * (self.j)

    def kut_izmedu_vektora(self, vektor):
        """Vraća kut između dvaju vektora u radijanima u rasponu od nula do pi."""
        return math.acos(self.skalarni_produkt(vektor)
                         / (self.duljina() * vektor.duljina()))

    def kut_izmedu_vektora360(self, vektor):
        """Vraća kut između dvaju vektora u radijanima u rasponu od nula do 2*pi."""
        skalarni_prod = self.skalarni_produkt(vektor)
        vektorski_prod = self.vektorski_produkt(vektor)
        kut = math.atan2(vektorski_prod, skalarni_prod)
        if kut < 0:
            kut += 2 * math.pi
        return kut


class Poligon:
    """Prikaz poligona u 2D koordinatnom sustavu

    Parametri
    ---------
    vrhovi: lista Tocaka
        Skup točaka čijim spajanjem po redu dobivamo željeni poligon.

    """

    def __init__(self, vrhovi):
        self.vrhovi = vrhovi

    def broj_vrhova(self):
        """Vraća broj vrhova poligona."""
        return len(self.vrhovi)

    def rubovi(self):
        """Vraća rubove poligona."""
        br_duzina = self.broj_vrhova()
        rubovi = []
        for i in range(0, br_duzina):
            rub_tocka_A = self.vrhovi[i % br_duzina]
            rub_tocka_B = self.vrhovi[(i + 1) % br_duzina]
            rub = Duzina(rub_tocka_A, rub_tocka_B)
            rubovi.append(rub)
        return rubovi

    def bool_operacije(self, drugi_poligon, operacija):
        """Izvršava Booleove operacije nad danim poligonima.

        Parametri
        ---------
        drugi_poligon: Poligon

        operacija: int
            Za dani broj izvršava određenu operaciju: -1 (razlika), 0 (unija),
             1 (presjek).

        Vraća
        -----
        rjesenje: lista Poligona
            Vraća listu svih poligona dobivenih zadanom operacijom.
        """
        # 1|. Promijena orijentacije po potrebi
        if operacija == -1:
            fragmenti_za_zadrzati_self = -1
            fragmenti_za_zadrzati_other = 1
            if self.orijentacija() == drugi_poligon.orijentacija():
                self.promijeni_orijentaciju()

        elif operacija == 0:
            fragmenti_za_zadrzati_self = -1
            fragmenti_za_zadrzati_other = -1
            if self.orijentacija() != drugi_poligon.orijentacija():
                self.promijeni_orijentaciju()

        elif operacija == 1:
            fragmenti_za_zadrzati_self = 1
            fragmenti_za_zadrzati_other = 1
            if self.orijentacija() != drugi_poligon.orijentacija():
                self.promijeni_orijentaciju()

        # 2|. Klasifikacija točaka
        pom_tocke_p_1 = [
            PomTocka(i, i.pripada_poligonu(drugi_poligon))
            for i in self.vrhovi
        ]
        pom_tocke_p_2 = [
            PomTocka(i, i.pripada_poligonu(self))
            for i in drugi_poligon.vrhovi
        ]

        # 3|. Pronalaženje sjecišta

        razvrstane_tocke_p_1 = pom_tocke_sjecista(pom_tocke_p_1,
                                                  pom_tocke_p_2)
        razvrstane_tocke_p_2 = pom_tocke_sjecista(pom_tocke_p_2,
                                                  pom_tocke_p_1)
        pom_tocke_p_1 = razvrstane_tocke_p_1
        pom_tocke_p_2 = razvrstane_tocke_p_2

        # 4|. Klasifikacija edge fragmenata

        razvrstani_fragmenti = (
            tocke_u_fragmente(
                pom_tocke_p_1,
                drugi_poligon,
                fragmenti_za_zadrzati_self,
                operacija)

            + tocke_u_fragmente(
                pom_tocke_p_2,
                self,
                fragmenti_za_zadrzati_other,
                operacija))

        # 5|. Odabir i organizacija fragmenata
        razvrstani_fragmenti = [i.duzina for i in razvrstani_fragmenti]

        povezani_fragmenti = povezi_fragmente(razvrstani_fragmenti)

        # 6|. Pretvorba fragmenata u tocke kako bi napravili poligone
        # nastali "oduzimanjem" dvaju poligona
        rjesenje = []

        for i in povezani_fragmenti:
            popis_razlika = []
            for j in i:
                popis_razlika.append(j.A)
            rjesenje.append(Poligon(popis_razlika))

        return rjesenje

    def orijentacija(self):
        """Vraća orijentaciju vrhova poligona."""
        zbroj = 0
        br_tocaka = self.broj_vrhova()
        for i in range(br_tocaka):
            zbroj += ((self.vrhovi[(i + 1) % br_tocaka].x
                      - self.vrhovi[i % br_tocaka].x)
                      * (self.vrhovi[(i + 1) % br_tocaka].y
                         + self.vrhovi[i % br_tocaka].y))
        return -1 + (zbroj > 0) * 2

    def promijeni_orijentaciju(self):
        """Mijenja orijentaciju vrhova poligona.

        Vraća
        -----
        :Poligon
            Vraća poligon s obrnutim redoslijedom vrhova.
        """
        obrnuti_redoslijed_tocaka = []
        br_tocaka = self.broj_vrhova()
        for i in range(br_tocaka):
            obrnuti_redoslijed_tocaka.append(self.vrhovi[(-i - 1) % br_tocaka])
        self.vrhovi = obrnuti_redoslijed_tocaka
        return Poligon(obrnuti_redoslijed_tocaka)

    def __sub__(self, other):
        """Booleova operacija oduzimanja (razlike)."""
        return self.bool_operacije(other, -1)

    def __add__(self, other):
        """Booleova operacija zbrajanja (unije)."""
        return self.bool_operacije(other, 0)

    def __mul__(self, other):
        """Booleova operacija množenja (presjeka)."""
        return self.bool_operacije(other, 1)

    def min_x(self):
        """Vraća najmanju apscisu svih vrhova poligona"""
        pom = self.vrhovi[0].x
        for i in self.vrhovi:
            if i.x < pom:
                pom = i.x
        return pom

    def max_x(self):
        """Vraća najveću apscisu svih vrhova poligona"""
        pom = self.vrhovi[0].x
        for i in self.vrhovi:
            if i.x > pom:
                pom = i.x
        return pom

    def min_y(self):
        """Vraća najmanju ordinatu svih vrhova poligona"""
        pom = self.vrhovi[0].y
        for i in self.vrhovi:
            if i.y < pom:
                pom = i.y
        return pom

    def max_y(self):
        """Vraća najveću ordinatu svih vrhova poligona"""
        pom = self.vrhovi[0].y
        for i in self.vrhovi:
            if i.y > pom:
                pom = i.y
        return pom

    def __repr__(self):
        """Prikaz objekta klase Poligon"""
        string = ""
        for t in self.vrhovi:
            string += "(%s , %s) " % (t.x, t.y)
        return string

    def __str__(self):
        """Prikaz objekta klase Poligon"""
        string = ""
        for t in self.vrhovi:
            string += "(%s , %s) " % (t.x, t.y)
        return string


class VoronoiCelija:
    """Prikaz Voronojeve ćelije

    Parametri
    ---------
    tocka: Tocka
        Prikaz točke koju okružuje Voronoi ćelija.

    poligon: Poligon
        Poligon koji predstavlja rubove Voronoi ćelije.

    """

    def __init__(self, tocka, poligon):
        self.tocka = tocka
        self.poligon = poligon


class PomTocka:
    """Pomoćna klasa sa položajem točke u poligonu.

    Pomoćna klasa za izvođenje Booleovih operacija koja sadrži neki objekt
    klase Tocka i njen položaj u odnosu na poligon (unutra, na rubu, vani).

    Parametri
    ---------
    tocka: Tocka

    polozaj: int
        Položaj točke u odnosu na neki poligon, odnosno nalazi li se
        točka unutar, izvan ili na rubu nekog poligona.
    """

    def __init__(self, tocka, polozaj):
        self.tocka = tocka
        self.polozaj = polozaj


class PomDuzina:
    """Pomoćna klasa sa položajem dužine u poligonu.

    Pomoćna klasa za izvođenje Booleovih operacija koja sadrži neki objekt
    klase Duzina i njen položaj u odnosu na poligon (unutra, na rubu, vani).

    Parametri
    ---------
    duzina: Duzina

    polozaj: int
        Položaj duzine u odnosu na neki poligon, odnosno nalazi li se
        točka unutar, izvan ili je rub nekog poligona.
    """

    def __init__(self, duzina, polozaj):
        self.duzina = duzina
        self.polozaj = polozaj


def pom_tocke_sjecista(pom_tocke_p_1, pom_tocke_p_2):
    """Traži sva sjecišta između poligona zadanih preko pomoćnih točaka.

    Parametri
    ---------
    pom_tocke_p_1,pom_tocke_p_2: lista PomTocaka
        Predstavljaju poredane vrhove poligona sa svojim položajima u odnosu na
        drugi poligon

    Vraća
    -----
    razrstane_tocke: lista PomTocaka
        Vraća početne liste pomoćnih točaka uz dodana novonađena sjecišta
        između poligona čiji su vrhovi zadani.
    """
    br_p_1 = len(pom_tocke_p_1)
    br_p_2 = len(pom_tocke_p_2)

    razvrstane_tocke = []
    for i in range(0, br_p_1):
        tocka_1_p_1 = pom_tocke_p_1[i % br_p_1]
        tocka_2_p_1 = pom_tocke_p_1[(i + 1) % br_p_1]
        stranica_p_1 = Duzina(tocka_1_p_1.tocka, tocka_2_p_1.tocka)

        pom_lista_tocaka = [tocka_1_p_1, tocka_2_p_1]

        for j in range(0, br_p_2):
            tocka_1_p_2 = pom_tocke_p_2[j % br_p_2]
            tocka_2_p_2 = pom_tocke_p_2[(j + 1) % br_p_2]
            stranica_p_2 = Duzina(tocka_1_p_2.tocka, tocka_2_p_2.tocka)

            sjec = stranica_p_1.sjeciste(stranica_p_2)

            if not sjec.prazna():
                pom_lista_tocaka.append(PomTocka(sjec, 0))

        pom_lista_tocaka = \
            sorted(pom_lista_tocaka,
                   key=lambda z:
                   (z.tocka.x - pom_lista_tocaka[0].tocka.x)**2
                   + (z.tocka.y - pom_lista_tocaka[0].tocka.y)**2)
        pom_lista_tocaka.pop(-1)

        for pom_tocka in pom_lista_tocaka:
            razvrstane_tocke.append(pom_tocka)

    return razvrstane_tocke


def tocke_u_fragmente(pom_tocke_p_1, p_2, trazeni_polozaj, operacija):
    """Spaja i klasificira razvrstane pomoćne točke u pomoćne dužine.

    Parametri
    ---------
    pom_tocke_p_1: lista PomTocaka

    p_2: Poligon

    trazeni_polozaj: int

    operacija: int
        Definira koju Booleovu operaciju izvodimo.

    Vraća
    -----
    fragmenti: lista PomDuzina
    """
    fragmenti = []
    br_p_1 = len(pom_tocke_p_1)
    for i in range(br_p_1):
        pom_tocka_1 = pom_tocke_p_1[i % br_p_1]
        pom_tocka_2 = pom_tocke_p_1[(i + 1) % br_p_1]
        if pom_tocka_1.tocka != pom_tocka_2.tocka:
            duzina = Duzina(pom_tocka_1.tocka, pom_tocka_2.tocka)
            if pom_tocka_1.polozaj == -1 or pom_tocka_2.polozaj == -1:
                polozaj = -1
            elif pom_tocka_1.polozaj == 1 or pom_tocka_2.polozaj == 1:
                polozaj = 1
            else:
                medutocka = Tocka(
                    (pom_tocka_1.tocka.x + pom_tocka_2.tocka.x) / 2,
                    (pom_tocka_1.tocka.y + pom_tocka_2.tocka.y) / 2)
                polozaj = medutocka.pripada_poligonu(p_2)

            nova_duzina = PomDuzina(duzina, polozaj)
            if (nova_duzina not in fragmenti
                    and polozaj == trazeni_polozaj
                    or (polozaj == 0
                        and operacija != -1
                        and nova_duzina not in fragmenti)):
                fragmenti.append(nova_duzina)
    return fragmenti


def povezi_fragmente(razvrstani_fragmenti):
    """Povezuje duzine tako da čine poligon."""
    povezani_fragmenti = []
    while len(razvrstani_fragmenti) > 0:

        novi_poligon = []
        novi_poligon.append(razvrstani_fragmenti[0])

        razvrstani_fragmenti.pop(razvrstani_fragmenti.index(novi_poligon[0]))

        i = 0
        while i < len(razvrstani_fragmenti):
            if ((abs(novi_poligon[-1].B.x
                     - razvrstani_fragmenti[i].A.x) < EPSILON)
                    and (abs(novi_poligon[-1].B.y
                             - razvrstani_fragmenti[i].A.y) < EPSILON)):
                novi_poligon.append(razvrstani_fragmenti[i])
                razvrstani_fragmenti.pop(i)
                i = -1
            i += 1

        povezani_fragmenti.append(novi_poligon)
    return povezani_fragmenti
