import math
import random
from greske import *

epsilon = 0.000001


class Tocka:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def __eq__(self, tocka):
        if(self.x is None or self.y is None
                or tocka.x is None or tocka.y is None):
            return self.x == tocka.x and self.y == tocka.y

        return abs(self.x-tocka.x)<epsilon and abs(self.y-tocka.y)<epsilon

    def __hash__(self):
        return hash(self.x+self.y)

    def __add__(self, other):
        return Tocka(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Tocka(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return "(%s , %s)" % (self.x, self.y)

    def __str__(self):
        return "(%s , %s)" % (self.x, self.y)

    def prazna(self):
        return self==Tocka(None,None)

    def mnozenje_skalarom(self,skalar):
        return Tocka(self.x * skalar, self.y * skalar)

    def lijevo_od(self,duzina):
        vektor = duzina.u_vektor()
        tocka = Duzina(duzina.B,self).u_vektor()
        return vektor.vektorski_produkt(tocka)>0

    # Prvo provjeravamo je li dana točka 'self'  jedna od točaka koja
    # omeđuje danu dužinu 'duzina'.  Danu dužinu 'duzina' pretvaramo u
    # vektor, a danu točku 'self' povezujemo s prvom točkom dane dužine
    # 'duzina' kako bi dobili novu dužinu.  Novonastalu dužinu pretvaramo u
    # vektor kako bi mogli izračunati vektorski produkt dviju dužina (sada
    # vektora).  Ako je vektorski produkt različit od nule, znači da dva
    # dana vektora nisu kolinearna pa ni dana točka ne pripada danoj dužini.
    # Određujemo duljinu dane dužine 'duzina' (ali ju ne korjenujemo pa
    # imamo "kvadratnu duljinu" dužine).  Određujemo skalarni produkt v1 i
    # v2 kako bi dobili duljinu ortagonalne projekcije (ali skalarni produkt
    # ne dijelimo s umnoškom duljina v1 i v2 pa dobijemo nešto kao "kvaratnu
    # duljinu").  Ako je kvadratna duljina == skalarni produkt, tada je
    # v1==v2, a ako je kvadratna duljina veća, tada v2 pripada v1, odnosno
    # točka pripada dužini.  Ako je skalarni produkt manji od 0 (negativna
    # je) tada je točka izvan dane dužine (na 'lijevo').  Ako je skalarni
    # produkt veći od kvadratne duljine, tada je točka izvan dane dužine (na
    # 'desno').
    #
    # IZVOR: [https://bit.ly/3R0hIBk]
    def pripada_duzini(self, duzina):
        if(self==duzina.A or self==duzina.B):
            return True

        v_1=duzina.u_vektor()
        v_2=Duzina(duzina.A,self).u_vektor()
        if(not v_1//v_2):
            return False

        skalarni_produkt=v_2.skalarni_produkt(v_1)
        if(skalarni_produkt<0):
            return False

        kvadratna_duljina=v_1.i**2+v_1.j**2
        return not(skalarni_produkt>kvadratna_duljina)

    # Za određivanje pripadnosti točke poligonu, iz dane točke se "povlači"
    # dužina paralelno s apcisom i provjerava se je li broj sjecišta između
    # te dužine i stranica poligona paran ili neparan.  Dužina
    # 'duzina_za_presjek' se sastoji od dane točke 'self' i najveće apcise
    # danog poligona 'poligon'.  Dužinu 'duzina_za_presjek' sječemo sa svim
    # stranicama poligona.  Ukoliko dužina 'duzina_za_presjek' nije paralelna
    # s danom stranicom poligona, traži se sjecište između dužine i stranice.
    # Sjecište se dodaje u ukupan zbroj sjecišta samo ako ono nije jedan od
    # vrhova poligona ILI ako sjecište jest jedan od vrhova poligona, ali taj
    # vrh je točka s manjom ordinatom stranice poligona.
    #
    # Moguće kombinacije stranica koje čine vrhove su /\, \/, <,>:
        # /\ ako se sjeće ovaj vrh, sjecištu se dodaje 0
            # (ne mijenja se parnost sjecišta)
        # \/ ako se sjeće ovaj vrh, sjecištu se dodaje 2
            # (ne mijenja se parnost sjecišta)
        # < ako se sjeće ovaj vrh, sjecištu se dodaje 1
            # (mijenja se parnost sjecišta)
        # > ako se sjeće ovaj vrh, sjecištu se dodaje 1
            # (mijenja se parnost sjecišta)
    #
    # Ukoliko su stranica i dužina 'duzina_za_presjek' paralelne, provjerava
    # se pripada li dana točka 'self' toj stranici poligona ili je točka
    # 'self' jedna od vrhova poligona.  Na kraju se provjerava je li broj
    # sjecišta paran (točka je van poligona) ili neparan (točka je u
    # poligonu).
    #
    # 0 - Točka je na rubu poligona
    # 1 - Točka je unutar poligona
    # -1 - Točka je izvan poligona
    #
    # IZVOR: [Computational Geometry: An Introduction, 41. str]
    def pripada_poligonu(self, poligon):
        najdesnija_tocka_plus = Tocka(poligon.max_x() + 1,self.y)
        if(najdesnija_tocka_plus==self):
            return -1

        duzina_za_presjek = Duzina(self, najdesnija_tocka_plus)
        rubovi_poligona = poligon.rubovi()
        sjecista = 0
        for rub in rubovi_poligona:
            if (self.pripada_duzini(rub)):
                return 0
            elif (not (rub.u_vektor() // duzina_za_presjek.u_vektor())):
                sjec = duzina_za_presjek.sjeciste(rub)
                if (not sjec.prazna()):
                    if (((sjec==rub.A or sjec==rub.B)
                         and sjec.y == rub.manja_oridnata())
                            or (sjec!=rub.A and sjec!=rub.B)):
                        sjecista += 1

        return 1 + (sjecista % 2 == 0) * -2

    def pripada_poligonu_wn(self, poligon):
        vrhovi_poligona = poligon.vrhovi
        br_tocaka = poligon.broj_vrhova()

        zbroj_kuteva = 0
        for i in range(0, br_tocaka):
            tocka_n = vrhovi_poligona[i]
            tocka_n_1 = vrhovi_poligona[(i + 1) % br_tocaka]
            rub_poligona = Duzina(tocka_n, tocka_n_1)

            if (self.pripada_duzini(rub_poligona)):
                return 0

            vektor_tocka_n= Duzina(self, tocka_n).u_vektor()
            vektor_tocka_n_1 = Duzina(self, tocka_n_1).u_vektor()

            vektor_tocka_yos = Duzina(self, self+Tocka(0,1)).u_vektor()

            kut = (vektor_tocka_n_1.kut_izmedu_vektora360(vektor_tocka_yos)
                   - vektor_tocka_n.kut_izmedu_vektora360(vektor_tocka_yos))

            if (kut > math.pi):
                kut -= 2 * math.pi

            if (kut < -math.pi):
                kut += 2 * math.pi

            zbroj_kuteva += kut

        if(abs(zbroj_kuteva)-epsilon<0 and abs(zbroj_kuteva)+epsilon>0):
            unutra = -1
        else:
            unutra = 1

        return unutra

    def udaljenost_od(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def polarni_kut(self, tocka):
        y_os_vektor = Duzina(self,
                             self + Tocka(1, 0)).u_vektor()
        pozicijski_vektor = Duzina(self,
                                   tocka).u_vektor()

        return y_os_vektor.kut_izmedu_vektora360(pozicijski_vektor)

class Duzina:
    def __init__(self, A, B):
        if(A!=B):
            self.A = A
            self.B = B
        else:
            raise IsteKrajnjeTockeError()

    def __hash__(self):
        return hash(self.A+self.B)

    def __eq__(self, other):
        return ((self.A==other.A and self.B==other.B)
                or (self.B == other.A and self.A == other.B))

    def __repr__(self):
        return "(%s , %s)" % (self.A, self.B)

    def __str__(self):
        return "(%s , %s)" % (self.A, self.B)

    def u_vektor(self):
        return Vektor((self.B-self.A).x,(self.B-self.A).y)


    # Ukoliko su dvije dužine paralelne, provjeravamo pripadaju li vrhovi
    # jedne dužine drugoj.  U suprotnome, računamo t i s.  t i s
    # predstavljaju koeficijente u jednadžbama dužina koji se kreću
    # od 0 do 1
    # [ pi = p1 + t(p2 - p1), pi = p3 + s(p4 - p3) ].
    #
    # pi - točka na dužini
    # p1,p2,p3,p4 - pozicijski vektori/točke
    #
    # Ako je 0<t,s<1 tada se dvije dužine sjeku.
    # IZVOR: [Mathematics for Computer Graphics, 274. str]
    def presjek(self, other):
        vektor_self = self.u_vektor()
        vektor_other = other.u_vektor()
        if (vektor_self // vektor_other):
            return (other.A.pripada_duzini(self)
                    or other.B.pripada_duzini(self)
                    or self.A.pripada_duzini(other)
                    or self.B.pripada_duzini(other))

        t = ((self.A.x * (other.B.y - other.A.y)
             + other.A.x * (self.A.y - other.B.y)
             + other.B.x * (other.A.y - self.A.y))
             / (vektor_other.vektorski_produkt(vektor_self)))

        s = ((self.A.x * (other.A.y - self.B.y)
             + self.B.x * (self.A.y - other.A.y)
             + other.A.x * (self.B.y - self.A.y))
             / (vektor_self.vektorski_produkt(vektor_other)))

        if (t >= 0 and t <= 1 and s >= 0 and s <= 1):
            return True

        return False

    #Isto kao presjek, ali umjesto True/False, vraća se sjecište, ako postoji
    def sjeciste(self, other):
        vektor_self = self.u_vektor()
        vektor_other = other.u_vektor()
        if (vektor_self // vektor_other):
            if (other.A.pripada_duzini(self)):
                return other.A
            elif (other.B.pripada_duzini(self)):
                return other.B
            elif(self.A.pripada_duzini(other)):
                return self.A
            elif (self.B.pripada_duzini(other)):
                return self.B
            else:
                return Tocka(None,None)

        t = ((self.A.x * (other.B.y - other.A.y)
              + other.A.x * (self.A.y - other.B.y)
              + other.B.x * (other.A.y - self.A.y))
             / (vektor_other.vektorski_produkt(vektor_self)))

        s = ((self.A.x * (other.A.y - self.B.y)
              + self.B.x * (self.A.y - other.A.y)
              + other.A.x * (self.B.y - self.A.y))
             / (vektor_self.vektorski_produkt(vektor_other)))

        if (t >= 0 and t <= 1 and s >= 0 and s <= 1):
            return self.A + (self.B - self.A).mnozenje_skalarom(t)

        return Tocka(None,None)

    def manja_oridnata(self):
        pom=self.A.y
        if(pom>self.B.y):
            pom=self.B.y
        return pom

    def veca_ordinata(self):
        pom = self.A.y
        if (pom < self.B.y):
            pom = self.B.y
        return pom

    def simetrala(self):
        tocka_A = self.A
        tocka_B = self.B

        daleka_tocka = 100000000

        srediste = Tocka((tocka_A.x + tocka_B.x) / 2,
                         (tocka_A.y + tocka_B.y) / 2)

        if (tocka_A.y == tocka_B.y):
            tocka_sim_A = Tocka(srediste.x, daleka_tocka)
            tocka_sim_B = Tocka(srediste.x, -daleka_tocka)

        elif (tocka_A.x == tocka_B.x):
            koeficijent = 0
            tocka_sim_A = \
                Tocka(daleka_tocka,
                      srediste.y + koeficijent * (daleka_tocka - srediste.x))
            tocka_sim_B = \
                Tocka(-daleka_tocka,
                      srediste.y + koeficijent * (-daleka_tocka - srediste.x))

        else:
            koeficijent = -1/((tocka_B.y - tocka_A.y) / (tocka_B.x - tocka_A.x))
            tocka_sim_A = \
                Tocka(daleka_tocka,
                      koeficijent * (daleka_tocka - srediste.x)+srediste.y)
            tocka_sim_B =\
                Tocka(-daleka_tocka,
                      koeficijent * (-daleka_tocka - srediste.x)+srediste.y)

        return Duzina(tocka_sim_A, tocka_sim_B)


class Vektor:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __add__(self, other):
        return Vektor(self.i + other.i, self.j + other.j)

    def __neg__(self):
        return Vektor(-self.i,-self.j)

    def __floordiv__(self, other):
        return self.vektorski_produkt(other)==0

    def __repr__(self):
        return "(%s , %s)" % (self.i, self.j)

    def __str__(self):
        return "(%s , %s)" % (self.i, self.j)

    def duljina(self):
        return (self.i**2+self.j**2)**(1/2)

    def skalarni_produkt(self,other):
        return self.i*other.i+self.j*other.j

    def vektorski_produkt(self, other):
        return (self.i) * (other.j) - (other.i) * (self.j)

    def kut_izmedu_vektora(self, other):
        return math.acos(self.skalarni_produkt(other)
                         / (self.duljina() * other.duljina()))

    def kut_izmedu_vektora360(self, other):
        skalarni_prod = self.skalarni_produkt(other)
        vektorski_prod = self.vektorski_produkt(other)
        kut = math.atan2(vektorski_prod, skalarni_prod)
        if (kut < 0):
            kut += 2 * math.pi
        return kut


class Poligon:
    def __init__(self,vrhovi):
        self.vrhovi=vrhovi

    def broj_vrhova(self):
        return len(self.vrhovi)

    def rubovi(self):
        br_duzina=self.broj_vrhova()
        rubovi = []
        for i in range(0, br_duzina):
            rub_tocka_A = self.vrhovi[i % br_duzina]
            rub_tocka_B = self.vrhovi[(i + 1) % br_duzina]
            rub = Duzina(rub_tocka_A,rub_tocka_B)
            rubovi.append(rub)
        return rubovi

    # IZVOR: [An algorithm for computing the union,
    # intersection or difference of two polygons]
    def bool_operacije(self, other, operacija):
        # 1|. Promijena orijentacije po potrebi
        if (operacija == -1):
            fragmenti_za_zadrzati_self = -1
            fragmenti_za_zadrzati_other = 1
            if (self.orijentacija() == other.orijentacija()):
                self.promijeni_orijentaciju()

        elif (operacija == 0):
            fragmenti_za_zadrzati_self = -1
            fragmenti_za_zadrzati_other = -1
            if (self.orijentacija() != other.orijentacija()):
                self.promijeni_orijentaciju()

        elif (operacija == 1):
            fragmenti_za_zadrzati_self = 1
            fragmenti_za_zadrzati_other = 1
            if (self.orijentacija() != other.orijentacija()):
                self.promijeni_orijentaciju()

        # 2|. Klasifikacija točaka
        pom_tocke_p_1 = [
            PomTocka(i, i.pripada_poligonu(other))
            for i in self.vrhovi
            ]
        pom_tocke_p_2 = [
            PomTocka(i, i.pripada_poligonu(self))
            for i in other.vrhovi
            ]

        # 3|. Pronalaženje sjecišta

        razvrstane_tocke_p_1 = pom_tocke_sjecista(pom_tocke_p_1,
                                                  pom_tocke_p_2)
        razvrstane_tocke_p_2 = pom_tocke_sjecista(pom_tocke_p_2,
                                                  pom_tocke_p_1)


        pom_tocke_p_1 = razvrstane_tocke_p_1
        pom_tocke_p_2 = razvrstane_tocke_p_2

        # 4|. Klasifikacija edge fragmenata

        razvrstani_fragmenti = (tocke_u_fragmente(pom_tocke_p_1,
                                                 other,
                                                 fragmenti_za_zadrzati_self,
                                                 operacija)
                               + tocke_u_fragmente(pom_tocke_p_2,
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

    # zašto ovo radi - [https://www.baeldung.com/cs/2d-polygon-area]
    def orijentacija(self):
        zbroj = 0
        br_tocaka = self.broj_vrhova()
        for i in range(br_tocaka):
            zbroj += ((self.vrhovi[(i + 1) % br_tocaka].x
                      - self.vrhovi[i % br_tocaka].x)
                     * (self.vrhovi[(i + 1) % br_tocaka].y
                        + self.vrhovi[i % br_tocaka].y))
        return -1+(zbroj>0)*2

    def promijeni_orijentaciju(self):
        obrnuti_redoslijed_tocaka = []
        br_tocaka=self.broj_vrhova()
        for i in range(br_tocaka):
            obrnuti_redoslijed_tocaka.append(self.vrhovi[(-i - 1) % br_tocaka])
        self.vrhovi=obrnuti_redoslijed_tocaka
        return Poligon(obrnuti_redoslijed_tocaka)

    def __sub__(self, other):
        return self.bool_operacije(other, -1)

    def __add__(self, other):
        return self.bool_operacije(other, 0)

    def __mul__(self, other):
        return self.bool_operacije(other, 1)

    def min_x(self):
        pom=self.vrhovi[0].x
        for i in self.vrhovi:
            if(i.x<pom):
                pom=i.x
        return pom

    def max_x(self):
        pom=self.vrhovi[0].x
        for i in self.vrhovi:
            if(i.x>pom):
                pom=i.x
        return pom

    def min_y(self):
        pom=self.vrhovi[0].y
        for i in self.vrhovi:
            if(i.y<pom):
                pom=i.y
        return pom

    def max_y(self):
        pom=self.vrhovi[0].y
        for i in self.vrhovi:
            if(i.y>pom):
                pom=i.y
        return pom

    def __repr__(self):
        string = ""
        for t in self.vrhovi:
            string+="(%s , %s) " % (t.x, t.y)
        return string

    def __str__(self):
        string = ""
        for t in self.vrhovi:
            string += "(%s , %s) " % (t.x, t.y)
        return string

class VoronoiCelija:
    def __init__(self, Tocka,Poligon):
        self.Tocka = Tocka
        self.Poligon = Poligon

class PomTocka:
    def __init__(self,tocka,polozaj):
        self.tocka=tocka
        self.polozaj=polozaj

class PomDuzina:
    def __init__(self,duzina,polozaj):
        self.duzina=duzina
        self.polozaj=polozaj


def pom_tocke_sjecista(pom_tocke_p_1,pom_tocke_p_2):
    br_p_1 = len(pom_tocke_p_1)
    br_p_2 = len(pom_tocke_p_2)

    razvrstane_tocke = []
    for i in range(0, br_p_1):
        tocka_1_p_1 = pom_tocke_p_1[i % br_p_1]
        tocka_2_p_1 = pom_tocke_p_1[(i + 1) % br_p_1]
        stranica_p_1 = Duzina(tocka_1_p_1.tocka, tocka_2_p_1.tocka)

        pom_lista_tocaka = []
        pom_lista_tocaka.append(tocka_1_p_1)
        pom_lista_tocaka.append(tocka_2_p_1)

        for j in range(0, br_p_2):
            tocka_1_p_2 = pom_tocke_p_2[j % br_p_2]
            tocka_2_p_2 = pom_tocke_p_2[(j + 1) % br_p_2]
            stranica_p_2 = Duzina(tocka_1_p_2.tocka, tocka_2_p_2.tocka)

            S = stranica_p_1.sjeciste(stranica_p_2)

            if (not S.prazna()):
                pom_lista_tocaka.append(PomTocka(S, 0))

        pom_lista_tocaka = \
            sorted(pom_lista_tocaka,
                   key=lambda z:
                   (z.tocka.x - pom_lista_tocaka[0].tocka.x)**2
                   + (z.tocka.y - pom_lista_tocaka[0].tocka.y)**2)
        pom_lista_tocaka.pop(-1)

        for j in pom_lista_tocaka:
            razvrstane_tocke.append(j)

    return razvrstane_tocke


def tocke_u_fragmente(pom_tocke_p_1,p_2,trazeni_polozaj,operacija):
    fragmenti = []
    br_p_1=len(pom_tocke_p_1)
    for i in range(br_p_1):
        pom_tocka_1 = pom_tocke_p_1[i%br_p_1]
        pom_tocka_2 = pom_tocke_p_1[(i+1)%br_p_1]
        if(pom_tocka_1.tocka!=pom_tocka_2.tocka):
            duzina=Duzina(pom_tocka_1.tocka,pom_tocka_2.tocka)
            if(pom_tocka_1.polozaj==-1 or pom_tocka_2.polozaj==-1):
                polozaj=-1
            elif(pom_tocka_1.polozaj==1 or pom_tocka_2.polozaj==1):
                polozaj=1
            else:
                medutocka=Tocka((pom_tocka_1.tocka.x+pom_tocka_2.tocka.x)/2,
                                (pom_tocka_1.tocka.y+pom_tocka_2.tocka.y)/2)
                polozaj=medutocka.pripada_poligonu(p_2)


            nova_duzina=PomDuzina(duzina,polozaj)
            if (nova_duzina not in fragmenti
                    and polozaj==trazeni_polozaj
                    or (polozaj==0
                        and operacija!=-1
                        and nova_duzina not in fragmenti)):
                fragmenti.append(nova_duzina)
    return fragmenti


def povezi_fragmente(razvrstani_fragmenti):
    povezani_fragmenti=[]
    while (len(razvrstani_fragmenti) > 0):

        novi_poligon = []
        novi_poligon.append(razvrstani_fragmenti[0])

        razvrstani_fragmenti.pop(razvrstani_fragmenti.index(novi_poligon[0]))

        i = 0
        while (i < len(razvrstani_fragmenti)):
            if ((abs(novi_poligon[-1].B.x
                    - razvrstani_fragmenti[i].A.x) < epsilon)
                    and (abs(novi_poligon[-1].B.y
                            - razvrstani_fragmenti[i].A.y) < epsilon)):
                novi_poligon.append(razvrstani_fragmenti[i])
                razvrstani_fragmenti.pop(i)
                i = -1
            i += 1

        povezani_fragmenti.append(novi_poligon)
    return povezani_fragmenti


def generiraj_broj(max=10):
    return (random.random() * 1000 % 2*max - max)


def nasumicna_tocka(max=10):
    return Tocka(generiraj_broj(max),generiraj_broj(max))


def nasumicne_tocke(broj_tocaka,max=10):
    tocke=[]
    while(len(tocke)<broj_tocaka and len(tocke)!=(2*max-1)*(2*max-1)):
        tocke.append(nasumicna_tocka(max))
        tocke=list(set(tocke))
    return tocke


def nasumicna_duzina(max=10):
    A = nasumicna_tocka(max)
    B = nasumicna_tocka(max)
    while(A==B):
        B=nasumicna_tocka(max)

    return Duzina(A,B)


def nasumicne_duzine(broj_duzina,max=10):
    duzine=[]
    while(len(duzine)<broj_duzina):
        duzine.append(nasumicna_duzina(max))
        duzine =list(set(duzine))
    return duzine


def nasumicni_poligon(broj_vrhova,max=10):
    return Poligon(nasumicne_tocke(broj_vrhova,max))


