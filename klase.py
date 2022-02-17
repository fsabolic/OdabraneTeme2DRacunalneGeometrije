class Tocka:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

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

# prvo provjeravamo je li dana točka 'self'  jedna od točaka koja omeđuje danu dužinu 'duzina'
# danu dužinu 'duzina' pretvaramo u vektor, a danu točku 'self' povezujemo s prvom točkom dane dužine 'duzina' kako bi dobili novu dužinu
# novonastalu dužinu pretvaramo u vektor kako bi mogli izračunati vektorski produkt dviju dužina (sada vektora)
# ako je vektorski produkt različit od nule, znači da dva dana vektora nisu kolinearna pa ni dana točka ne pripada danoj dužini
# određujemo duljinu dane dužine 'duzina' (ali ju ne korjenujemo pa imamo "kvadratnu duljinu" dužine)
# određujemo skalarni produkt v1 i v2 kako bi dobili duljinu ortagonalne projekcije (ali skalarni produkt ne dijelimo s umnoškom duljina v1 i v2 pa dobijemo nešto kao "kvaratnu duljinu")
# ako je kvadratna duljina == skalarni produkt, tada je v1==v2, a ako je kvadratna duljina veća, tada v2 pripada v1, odnosno točka pripada dužini
# ako je skalarni produkt manji od 0 (negativna je) tada je točka izvan dane dužine (na 'lijevo')
# ako je skalarni produkt veći od kvadratne duljine, tada je točka izvan dane dužine (na 'desno')
    def pripada_duzini(self, duzina):

        if(self==duzina.A or self==duzina.B):
            return True

        v_1=duzina.u_vektor()
        v_2=Duzina(duzina.A,self).u_vektor()
        if(v_1.vektorski_produkt(v_2)!=0):
            return False

        kvadratna_duljina=v_1.i**2+v_1.j**2
        skalarni_produkt=v_2.skalarni_produkt(v_1)
        if(skalarni_produkt<0):
            return False

        return not(skalarni_produkt>kvadratna_duljina)

# za određivanje pripadnosti točke poligonu, iz dane točke se "povlači" dužina paralelno s apcisom i provjerava se je li broj sjecišta između te dužine i stranica poligona paran ili neparan
# dužina 'duzina_za_presjek' se sastoji od dane točke 'self' i najveće apcise danog poligona 'poligon'
# dužinu 'duzina_za_presjek' sječemo sa svim stranicama poligona
# ukoliko dužina 'duzina_za_presjek' nije paralelna s danom stranicom poligona, traži se sjecište između dužine i stranice
# sjecište se dodaje u ukupan zbroj sjecišta samo ako ono nije jedan od vrhova poligona ILI ako sjecište jest jedan od vrhova poligona, ali taj vrh je točka s manjom ordinatom stranice poligona
# moguće kombinacije stranica koje čine vrhove su /\, \/, <,>:
    # /\ ako se sjeće ovaj vrh, sjecištu se dodaje 0 (ne mijenja se parnost sjecišta)
    # \/ ako se sjeće ovaj vrh, sjecištu se dodaje 2 (ne mijenja se parnost sjecišta)
    # < ako se sjeće ovaj vrh, sjecištu se dodaje 1 (mijenja se parnost sjecišta)
    # > ako se sjeće ovaj vrh, sjecištu se dodaje 1 (mijenja se parnost sjecišta)
# ukoliko su stranica i dužina 'duzina_za_presjek' paralelne, provjerava se pripada li dana točka 'self' toj stranici poligona ili je točka 'self' jedna od vrhova poligona
# na kraju se provjerava je li broj sjecišta paran (točka je van poligona) ili neparan (točka je u poligonu)
#[Computational Geometry: An Introduction, 41. str]
    def pripada_poligonu(self,poligon):
        duzina_za_presjek = Duzina(self, Tocka(poligon.max_x() + 1, self.y))
        skup_stranica_poligona = poligon.u_duzine()
        sjecista = 0
        for i in skup_stranica_poligona:
            if (not (i.u_vektor() // duzina_za_presjek.u_vektor())):
                S = duzina_za_presjek.sjeciste(i)
                if (S != Tocka(None, None)):
                    if ((S in poligon.tocke and S.y == i.manja_oridnata()) or (S not in poligon.tocke)):
                        sjecista += 1
            else:
                if (self.pripada_duzini(i) or self in poligon.tocke):
                    return True

        return sjecista % 2 != 0

class Duzina:
    def __init__(self, A, B):
        if(A!=B):
            self.A = A
            self.B = B
        else:
            raise ValueError('Dužina ne može biti zadana dvjema točkama koje su jednake')

    def __eq__(self, other):
        return (self.A==other.A and self.B==other.B) or (self.B==other.A and self.A==other.B)

    def __repr__(self):
        return "(%s , %s)" % (self.A, self.B)

    def __str__(self):
        return "(%s , %s)" % (self.A, self.B)

    def u_vektor(self):
        return Vektor((self.B-self.A).x,(self.B-self.A).y)

#ukoliko su dvije dužine paralelne, provjeravamo pripadaju li vrhovi jedne dužine drugoj
#u suprotnome, računamo t i s
#t i s predstavljaju koeficijente u jednadžbama dužina koji se kreću od 0 do 1 [ pi = p1 + t(p2 - p1), pi = p3 + s(p4 - p3) ]
    #pi - točka na dužini
    #p1,p2,p3,p4 - pozicijski vektori/točke
#ako je 0<t,s<1 tada se dvije dužine sjeku
#[Mathematics for Computer Graphics, 274. str]
    def presjek(self, other):
        vektor_self = self.u_vektor()
        vektor_other = other.u_vektor()
        if (vektor_self // vektor_other):
            return other.A.pripada_duzini(self) or other.B.pripada_duzini(self) or self.A.pripada_duzini(other) or self.B.pripada_duzini(other) #pripazit na ovo, dal radi???

        t = (self.A.x * (other.B.y - other.A.y) + other.A.x * (self.A.y - other.B.y) + other.B.x * (other.A.y - self.A.y)) / (
            vektor_other.vektorski_produkt(vektor_self))

        s = (self.A.x * (other.A.y - self.B.y) + self.B.x * (self.A.y - other.A.y) + other.A.x * (self.B.y - self.A.y)) / (
            vektor_self.vektorski_produkt(vektor_other))

        if (t >= 0 and t <= 1 and s >= 0 and s <= 1):
            return True

        return False

#isto kao presjek, ali umjesto True/False, vraća se sjecište, ako postoji
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

        t = (self.A.x * (other.B.y - other.A.y) + other.A.x * (self.A.y - other.B.y) + other.B.x * (other.A.y - self.A.y)) / (
            vektor_other.vektorski_produkt(vektor_self))

        s = (self.A.x * (other.A.y - self.B.y) + self.B.x * (self.A.y - other.A.y) + other.A.x * (self.B.y - self.A.y)) / (
            vektor_self.vektorski_produkt(vektor_other))

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

class Vektor:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __add__(self, other):
        return Vektor(self.i + other.i, self.j + other.j)

    def __neg__(self):
        return Vektor(-self.i,-self.j)

    def __floordiv__(self, other):
        if(other.i==0 and self.i!=0):
            if(self.j==0):
                return False
            else:
                return (other.i/self.i)*other.j==self.j

        elif(other.i==0 and self.i==0):
            if(self.j!=0 and other.j!=0):
                return True
            else:
                return False

        return (self.i/other.i)*other.j==self.j

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

class Poligon:

    def __init__(self,tocke):
        self.tocke=tocke

    def u_duzine(self):
        br_duzina=len(self.tocke)
        return [Duzina(self.tocke[i%br_duzina],self.tocke[(i+1)%br_duzina]) for i in range(0,br_duzina)]

    def broj_tocaka(self):
        return len(self.tocke)

    def min_x(self):
        pom=self.tocke[0].x
        for i in self.tocke:
            if(i.x<pom):
                pom=i.x
        return pom

    def max_x(self):
        pom=self.tocke[0].x
        for i in self.tocke:
            if(i.x>pom):
                pom=i.x
        return pom

    def min_y(self):
        pom=self.tocke[0].y
        for i in self.tocke:
            if(i.y<pom):
                pom=i.y
        return pom

    def max_y(self):
        pom=self.tocke[0].y
        for i in self.tocke:
            if(i.y>pom):
                pom=i.y
        return pom

