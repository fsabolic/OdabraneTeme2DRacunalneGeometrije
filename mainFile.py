# # from booloperacije import *
# # from konveksnaljuska import *
# #
# # def razdvoji_tocke(tocke):
# #     tocke.sort(key=lambda tocka: tocka.x)
# #
# #     tocke_l = []
# #     tocke_d = []
# #
# #     for i in range(0,int(len(tocke)/2)):
# #        tocke_l.append(tocke[i])
# #
# #     for i in range(int(len(tocke)/2),len(tocke)):
# #        tocke_d.append(tocke[i])
# #
# #     return tocke_l,tocke_d
# #
# # def Dac(tocke):
# #     if(len(tocke)>3):
# #         tocke_l,tocke_d = razdvoji_tocke(tocke)
# #         Dac(tocke_l)
# #         Dac(tocke_d)
# #         print(tocke_l)
# #         print(tocke_d)
# #         print("---------------------------------------------------------------------")
# #     else:
# #         return
# #
# # tocke=[Tocka(random()*1000%20-10,random()*1000%20-10) for i in range(11)]
# #
# # tocke = list(set(tocke))
# # tocke.sort(key=lambda tocka: tocka.x)
# #
# # tocke_l,tocke_d = razdvoji_tocke(tocke)
# #
# # ax.scatter([i.x for i in tocke_l], [i.y for i in tocke_l], color="red")
# #
# # ax.scatter([i.x for i in tocke_d], [i.y for i in tocke_d], color="blue")
# #
# # Dac(tocke)
# #
# #
# #
# # plt.show()
# import math
#
# import matplotlib.pyplot as plt
# from random import *
# from klase import *
# from konveksnaljuska import *
#
# def razdvoji_tocke(tocke):
#     tocke.sort(key=lambda tocka: tocka.x)
#
#     tocke_l = []
#     tocke_d = []
#
#     for i in range(0,int(len(tocke)/2)):
#        tocke_l.append(tocke[i])
#
#     for i in range(int(len(tocke)/2),len(tocke)):
#        tocke_d.append(tocke[i])
#
#     return tocke_l,tocke_d
#
#
# #funkcija za pronalaženje simetrale dane dužine, vraća dužinu koja je dovoljno dugačka da ju možemo promatrati kao pravac...
# # prvo uzimamo točke dviju dužina i tražimo središte te dužine
# # nakon toga određujemo koeficijent smjera pravca na kojem se dužina nalazi i tražimo koeficijent smjera okomitog pravca
# # postoje 2 edgecase-a za pronalaženje koeficijenta smjera:
# #       pravac je vertikalan : koeficijent smjera je nula
# #       pravac je horizontalan : koeficijent smjera je "beskonačan"
# #   - u oba slućaja, točke koje omeđuju dužinu ćemo "ručno" stvoriti
# # ako se ne radi o edgecase-u, pronalazimo koeficijent pravca, računamo koeifcijent okomitog pravca i pronalazimo dvije točke na tom pravcu (obje točke moraju biti "daleko")
# # nema literature!
# def simetrala(duzina):
#     a = duzina.A
#     b = duzina.B
#
#     srediste = Tocka((a.x + b.x) / 2, (a.y + b.y) / 2)
#
#     if (a.y == b.y):
#         tocka_prva = Tocka(srediste.x, 100000000)
#         tocka_druga = Tocka(srediste.x, -100000000)
#
#     elif (a.x == b.x):
#         koeficijent = 0
#         tocka_prva = Tocka(100000000, srediste.y + koeficijent * (100000000 - srediste.x))
#         tocka_druga = Tocka(-100000000, srediste.y + koeficijent * (-100000000- srediste.x))
#
#     else:
#         koeficijent = -1 / ((b.y - a.y) / (b.x - a.x))
#         tocka_prva = Tocka(100000000, srediste.y + koeficijent * (100000000 - srediste.x))
#         tocka_druga = Tocka(-100000000, srediste.y + koeficijent * (-100000000- srediste.x))
#
#     return Duzina(tocka_prva,tocka_druga)
#
# # funkcija za traženje voronojevog dijagrama koji se sastoji od 2 ili 3 točke, a vraća "rubove" (dužine) od kojih se sastoji voronojev dijagram
# #  postoje 2 edgecase-a:
# #       1. proslijeđene su dvije točke : vratit će se samo simetrala dužine koje čine te dvije točke
# #       2. proslijeđene su tri koolinearne točke : vratiti će se simetrale dviju dužina -> dužina AB i dužina BC gdje su točke sortirane po x koordinati od najmanje prema najvećoj (A.x < B.x < C.x)
# # u ostalim slučajevima provodi se "normalna" konstrukcija Voronoievog dijagrama
# # pronalazimo dužine koje čine prva i druga točka te druga i treća točka (prva točka je relativan pojam jer ne mora biti prva u listi, nego prva točkan na koju pokazuje varijabla "i")
# # nakon toga tražimo simetrale tih dužina i njihovo sjecište
# # kako bi pronašli koju "polovicu" koje simetrale želimo zadržati kao jedan od rubova dijagrama, pokušavamo pronaći udaljenost od jedne točke (A) dužine čija je simetrala do određene točke na simetrali i udaljenost treće točke (ona od koje se ne sastoji dužina simetrale, C) do iste točke na simetrali
# # ako je udaljenost od A manja od udaljenosti od C, tada zadržavamo tu polovicu simetrale, a odbacujemo drugu
# # u suprotnome zadržavamo drugu polovicu simetrale
#
# #Literatura: [???] Ne znam otkud mi ovo iskreno, al našo sam objašnjenje tu: https://www.youtube.com/watch?v=j2c3kumwoAk
# def voronoi(lista_tocaka):
#     rubovi = []
#     broj_tocaka = len(lista_tocaka)
#
#     if(broj_tocaka==2):
#         tocka_1 = lista_tocaka[0]
#         tocka_2 = lista_tocaka[1]
#         rubovi.append(simetrala(Duzina(tocka_1,tocka_2)))
#
#     elif(broj_tocaka==3):
#         kut_medu_vektorima = Duzina(lista_tocaka[0], lista_tocaka[1]).u_vektor().kut_izmedu_vektora(
#             Duzina(lista_tocaka[1], lista_tocaka[2]).u_vektor())
#         if(kut_medu_vektorima==0 or kut_medu_vektorima==3*math.pi/2):
#             lista_tocaka.sort(key=lambda tocka: tocka.x)
#             rubovi.append(simetrala(Duzina(lista_tocaka[0],lista_tocaka[1])))
#             rubovi.append(simetrala(Duzina(lista_tocaka[1],lista_tocaka[2])))
#         else:
#             for i in range(0,broj_tocaka):
#                 A= lista_tocaka[i%broj_tocaka]
#                 B = lista_tocaka[(i+1)%broj_tocaka]
#                 C= lista_tocaka[(i+2)%broj_tocaka]
#
#                 duzina_AB = Duzina(A, B)
#                 simetrala_AB = simetrala(duzina_AB)
#
#                 duzina_BC = Duzina(B, C)
#                 simetrala_BC = simetrala(duzina_BC)
#
#                 sjeciste_AB_BC= simetrala_AB.sjeciste(simetrala_BC)
#
#                 duljina_1 = Duzina(A, simetrala_AB.A).u_vektor().duljina()
#                 duljina_2 = Duzina(C, simetrala_AB.A).u_vektor().duljina()
#
#                 if (duljina_1< duljina_2):
#                     rubovi.append(Duzina(sjeciste_AB_BC,simetrala_AB.A))
#
#                 else:
#                     rubovi.append(Duzina(sjeciste_AB_BC, simetrala_AB.B))
#
#     for rub in rubovi:
#         plt.plot([rub.A.x, rub.B.x], [rub.A.y, rub.B.y], color="black")
#
#     return rubovi
#
#
# def pronadi_pomocne_segmente_ljudski(l,d):
#
#     prva = Poligon(konveksna_ljuska(l+d)).u_duzine()
#
#     druga = Poligon(konveksna_ljuska(l)).u_duzine()
#
#     treca = Poligon(konveksna_ljuska(d)).u_duzine()
#
#     v_konveksna_ljuska(l)
#     v_konveksna_ljuska(d)
#
#     for duzina in druga:
#         for duzina2 in prva:
#             if(duzina==duzina2):
#                 prva.remove(duzina2)
#
#     for duzina in treca:
#         for duzina2 in prva:
#             if(duzina==duzina2):
#                 prva.remove(duzina2)
#
#     gd = 0
#     dd = 0
#     gl = 0
#     dl = 0
#
#     if((prva[0].A.y+prva[0].B.y)>(prva[1].A.y+prva[1].B.y)):
#         if(prva[0].A.x<prva[0].B.x):
#             gl = prva[0].A
#             gd = prva[0].B
#         else:
#             gl = prva[0].B
#             gd = prva[0].A
#         if(prva[1].A.x<prva[1].B.x):
#             dl = prva[1].A
#             dd = prva[1].B
#         else:
#             dl = prva[1].B
#             dd = prva[1].A
#     else:
#         if(prva[1].A.x<prva[1].B.x):
#             gl = prva[1].A
#             gd = prva[1].B
#         else:
#             gl = prva[1].B
#             gd = prva[1].A
#         if(prva[0].A.x<prva[0].B.x):
#             dl = prva[0].A
#             dd = prva[0].B
#         else:
#             dl = prva[0].B
#             dd = prva[0].A
#
#     pom_gd = [i for i in d if i!=gd and (Duzina(gl,gd).u_vektor()//Duzina(gd,i).u_vektor())]
#     pom_gl = [i for i in l if i != gl and (Duzina(gl,gd).u_vektor()//Duzina(gd,i).u_vektor())]
#     pom_dd = [i for i in d if i != dd and (Duzina(dl,dd).u_vektor()//Duzina(dd,i).u_vektor())]
#     pom_dl = [i for i in l if i != dl and (Duzina(dl,dd).u_vektor()//Duzina(dd,i).u_vektor())]
#
#     pom_gd.append(gd)
#     pom_gl.append(gl)
#     pom_dd.append(dd)
#     pom_dl.append(dl)
#
#     pom_gd.sort(key=lambda tocka:tocka.x)
#     pom_gl.sort(key=lambda tocka:tocka.x,reverse=True)
#     pom_dd.sort(key=lambda tocka:tocka.x)
#     pom_dl.sort(key=lambda tocka:tocka.x,reverse=True)
#
#     gd = pom_gd[0]
#     gl = pom_gl[0]
#     dd = pom_dd[0]
#     dl = pom_dl[0]
#
#
# #    for t in prva:
# #        plt.plot([t.A.x,t.B.x],[t.A.y,t.B.y],color="red")
#     plt.plot([gl.x,gd.x],[gl.y,gd.y],color="red")
#     plt.plot([dl.x,dd.x],[dl.y,dd.y],color="red")
#     plt.scatter(gd.x,gd.y, color="yellow")
#     plt.scatter(gl.x, gl.y, color="green")
#     plt.scatter(dd.x, dd.y, color="pink")
#     plt.scatter(dl.x, dl.y, color="blue")
#
#     duzina_gore = Duzina(gl,gd)
#
#     duzina_dole = Duzina(dl,dd)
#
#     simetrala_gore = simetrala(duzina_gore)
#
#     simetrala_dole = simetrala(duzina_dole)
#
#
#     if(simetrala_gore.A.y>(duzina_gore.A.y+duzina_gore.B.y)/2):
#       polusimetrala_gore = Duzina(simetrala_gore.A,simetrala_gore.sjeciste(duzina_gore))
#
#     else:
#         polusimetrala_gore = Duzina(simetrala_gore.B, simetrala_gore.sjeciste(duzina_gore))
#
#     if (simetrala_dole.A.y <(duzina_dole.A.y + duzina_dole.B.y) / 2):
#         polusimetrala_dole = Duzina(simetrala_dole.A, simetrala_dole.sjeciste(duzina_dole))
#
#     else:
#         polusimetrala_dole = Duzina(simetrala_dole.B, simetrala_dole.sjeciste(duzina_dole))
#
#     plt.plot([polusimetrala_gore.A.x,polusimetrala_gore.B.x],[polusimetrala_gore.A.y,polusimetrala_gore.B.y],color="black",linestyle="dashed")
#     plt.plot([polusimetrala_dole.A.x, polusimetrala_dole.B.x], [polusimetrala_dole.A.y, polusimetrala_dole.B.y],color="black", linestyle="dashed")
#     plt.scatter(simetrala_gore.sjeciste(duzina_gore).x,simetrala_gore.sjeciste(duzina_gore).y,color="black")
#     plt.scatter(simetrala_dole.sjeciste(duzina_dole).x,simetrala_dole.sjeciste(duzina_dole).y,color="black")
#
#
#     return {"gornja":polusimetrala_gore,"donja":polusimetrala_dole}
#
# def generiraj_broj():
#     max =10
#     return random() * 1000 % 2*max - max
#
# j=0
# while(j<1):
#
#     #tocka_1 = Tocka(3,2)
#     #tocka_2 = Tocka(2,6)
#     #tocka_3 = Tocka(3,-5)
#     if(j%100==0):
#         print(j)
#     tocka_1 = Tocka(1,1)
#     tocka_2 = Tocka(1,1)
#     tocka_3 = Tocka(1,1)
#
#     tocke = []
#     # while(len(list(set(tocke)))<6):
#     #     tocka_1 = Tocka(int(random()*1000%20-10),int(random()*1000%20-10))
#     #     tocka_2 = Tocka(int(random()*1000%20-10),int(random()*1000%20-10))
#     #     tocka_3 = Tocka(int(random()*1000%20-10),int(random()*1000%20-10))
#     #     tocka_4 = Tocka(int(random()*1000%20-10),int(random()*1000%20-10))
#     #     tocka_5 = Tocka(int(random()*1000%20-10),int(random()*1000%20-10))
#     #     tocka_6 = Tocka(int(random()*1000%20-10),int(random()*1000%20-10))
#     #     tocke = [tocka_1,tocka_2,tocka_3,tocka_4,tocka_5,tocka_6]
#     #
#     # for i in range(0,15):
#     #     tocke.append(Tocka(int(random()*1000%20-10),int(random()*1000%20-10)))
#
#     while(len(list(set(tocke)))<6):
#         tocka_1 = Tocka(generiraj_broj(),generiraj_broj())
#         tocka_2 = Tocka(generiraj_broj(),generiraj_broj())
#         tocka_3 = Tocka(generiraj_broj(),generiraj_broj())
#         tocka_4 = Tocka(generiraj_broj(),generiraj_broj())
#         tocka_5 = Tocka(generiraj_broj(),generiraj_broj())
#         tocka_6 = Tocka(generiraj_broj(),generiraj_broj())
#         tocke = [tocka_1,tocka_2,tocka_3,tocka_4,tocka_5,tocka_6]
#
#     for i in range(0,int(random()*1000%20)):
#
#         tocka = Tocka(generiraj_broj(),generiraj_broj())
#         while(tocke.count(tocka)>0):
#             tocka = Tocka(generiraj_broj(), generiraj_broj())
#         tocke.append(tocka)
#
#     l,d = razdvoji_tocke(tocke)
#
#
#     dict = pronadi_pomocne_segmente_ljudski(l,d)
#
#     gornja = dict["gornja"]
#     donja = dict["donja"]
#
#
#     j+=1
#
# plt.show()
#
#
#
import matplotlib.pyplot as plt
from presjeksegmenata import *
from booloperacije import *
from konveksnaljuska import *
from math import *

# print(v_presjek(Poligon([Tocka(0,0),Tocka(6,0),Tocka(6,6),Tocka(0,6),]),Poligon([Tocka(0,0),Tocka(0,6),Tocka(-6,6),Tocka(-6,0),])))
# print(Poligon([Tocka(0,0),Tocka(6,0),Tocka(6,6),Tocka(0,6),]).bool_operacije(Poligon([Tocka(0,0),Tocka(0,6),Tocka(-6,6),Tocka(-6,0),]),1))

def simetrala(duzina):
    a = duzina.A
    b = duzina.B

    srediste = Tocka((a.x + b.x) / 2, (a.y + b.y) / 2)

    if (a.y == b.y):
        tocka_prva = Tocka(srediste.x, 100000000)
        tocka_druga = Tocka(srediste.x, -100000000)

    elif (a.x == b.x):
        koeficijent = 0
        tocka_prva = Tocka(100000000, srediste.y + koeficijent * (100000000 - srediste.x))
        tocka_druga = Tocka(-100000000, srediste.y + koeficijent * (-100000000- srediste.x))

    else:
        koeficijent = -1 / ((b.y - a.y) / (b.x - a.x))
        tocka_prva = Tocka(100000000, srediste.y + koeficijent * (100000000 - srediste.x))
        tocka_druga = Tocka(-100000000, srediste.y + koeficijent * (-100000000- srediste.x))

    return Duzina(tocka_prva,tocka_druga)

def udaljenost_tocke(tocka_a,tocka_b):
    return sqrt((tocka_a.x-tocka_b.x)**2+(tocka_a.y-tocka_b.y)**2)

def generiraj_broj():
    max = 2
    return int(random() * 1000 % 2*max - max)

def kut360(vektor1,vektor2):
    sp = vektor1.skalarni_produkt(vektor2)
    det = vektor1.i*vektor2.j-vektor1.j*vektor2.i
    kut =  atan2(det,sp)
    if(kut < 0):

        kut += 2*pi

    return  kut

class VoronoiCelija:
    def __init__(self, Tocka,Poligon):
        self.Tocka = Tocka
        self.Poligon = Poligon

tocke = []

while(len(tocke)<3):
    tocke = [Tocka(generiraj_broj(),generiraj_broj()) for i in range(0,21)]

# tocke = [
#
#
#     Tocka(9,3),
#     Tocka(-5,-5),
#     Tocka(4, -3),
#
#     Tocka(-6, 4),
#     Tocka(1, 3),
#     Tocka(1, 0),
#     Tocka(-3, 9),
#     Tocka(2, 6),
#     Tocka(-4, 6),
#     Tocka(2,-2),
#     Tocka(7,0),
#  ]

#tocke =[   Tocka(-2 , 9),Tocka(6 , 4),Tocka(4 , -8), ]
# #
#tocke = [Tocka(-7 , -6),Tocka(-2 , -2),Tocka(-1 , 5)]
#
#tocke = [Tocka(3 , 1), Tocka(0 , 4), Tocka(0 , -2)]
#
#tocke = [ Tocka(-1 , 2), Tocka(0 , 3),Tocka(-2 , -1), Tocka(0 , -1),]
#
#
#tocke = [Tocka(1,0),Tocka(3,3),Tocka(0,-3),Tocka(0,-5),Tocka(4,-5),]
#
#
#tocke = [Tocka(5 , -8), Tocka(2 , -8), Tocka(1 , -4), Tocka(9 , 2), Tocka(-7 , -7), Tocka(-8 , 7),]
#
#tocke = [ Tocka(0 , 7),Tocka(-9 , -5),Tocka(-3 , 0), Tocka(1 , -8),Tocka(4 , 2),  Tocka(7 , 0), ]
#
#tocke = [Tocka(-2 , -3), Tocka(-9 , -1), Tocka(8 , -5), Tocka(-5 , 8), Tocka(-4 , 9)]
#
#tocke =[Tocka(9 , -7),Tocka(-7 , -4), Tocka(0 , 5), Tocka(9 , -4),  Tocka(6 , 6)]




#tocke = [Tocka(5 , -7), Tocka(1 , -7), Tocka(-1 , -8), Tocka(-3 , -9), Tocka(6 , 2)]
#tocke =  [ Tocka(5 , -3), Tocka(5 , 5),Tocka(5 , -8), Tocka(8 , 6), Tocka(-3 , 9)]

#tocke = [Tocka(0 , -2), Tocka(1 , -2), Tocka(0 , -4), Tocka(-1 , 0), Tocka(-3 , 0), Tocka(-4 , -2), Tocka(-4 , -1), Tocka(3 , 4), Tocka(-4 , 4)]
# tocke = [Tocka(-8 , 8), Tocka(-3 , -5), Tocka(7 , 2)]
#
#tocke = [Tocka(-4 , 0), Tocka(4 , 9), Tocka(2 , 4)]
#
#tocke = [Tocka(9 , 0), Tocka(9 , 2), Tocka(-5 , 0)]
#
#tocke = [Tocka(-1 , -7), Tocka(2 , 0), Tocka(7 , 4)]
#
#tocke = [Tocka(8 , -5), Tocka(-5 , -6), Tocka(-4 , 3)]
#
#tocke = [Tocka(4 , 8), Tocka(-8 , -4), Tocka(5 , 2)]
#
#tocke = [Tocka(6 , 4), Tocka(4 , -8), Tocka(-2 , 9)]
#
#tocke = [Tocka(-4 , 4), Tocka(6 , -3), Tocka(-8 , 6)]
#
#
#
#tocke = [Tocka(3 , 1), Tocka(0 , 4), Tocka(0 , -2)]
#
#tocke = [Tocka(-1 , 2), Tocka(0 , 3), Tocka(-2 , -1), Tocka(0 , -1)]
#
#
#  tocke = [ Tocka(0,1), Tocka(-2,0), Tocka(0,-3), Tocka(3,4)]
#
#tocke = [ Tocka(1,0), Tocka(3,3), Tocka(0,-3), Tocka(0,-5), Tocka(4,-5),]
#
#tocke = [Tocka(-3.1683908934753617 , -4.653706072281693), Tocka(-4.355690592880592 , 0.6006362024813825), Tocka(-0.9136761660038246 , 4.3713870698911705), Tocka(1.9514248983439302 , 3.7028994697220696), Tocka(1.7354732689213108 , 4.111435949275574), Tocka(5.004579181639201 , 3.56763219487857)]
# #
# #
# #
# tocke = [Tocka(5 , -8), Tocka(5 , -3), Tocka(5 , 5), Tocka(8 , 6), Tocka(-3 , 9)]
# #
# tocke = [Tocka(-2 , -3), Tocka(-9 , -1), Tocka(8 , -5), Tocka(-5 , 8), Tocka(-4 , 9)]
# #
# tocke = [Tocka(5 , -7), Tocka(1 , -7), Tocka(-1 , -8), Tocka(-3 , -9), Tocka(6 , 2)]
# #
#tocke = [Tocka(-7 , 5), Tocka(-2 , 6), Tocka(-6 , -1), Tocka(-7 , -2), Tocka(0 , 8), Tocka(3 , 3), Tocka(-9 , -9), Tocka(3 , -7)]
# #
# tocke = [Tocka(-7 , -4), Tocka(0 , 5), Tocka(9 , -4), Tocka(9 , -7), Tocka(6 , 6)]
# #
#tocke = [Tocka(-1 , -2),Tocka(2 , -2), Tocka(1 , -1),  Tocka(0 , -1)]
# #
# tocke = [Tocka(1 , 1), Tocka(2 , 0), Tocka(1 , -1), Tocka(2 , -1)]

#tocke = [Tocka(-1,0),Tocka(0,0),Tocka(-2,2),Tocka(-2,1),Tocka(0,2),Tocka(0,1),Tocka(-1,1),Tocka(-1,2),Tocka(-2,0),]

#tocke = [Tocka(2 , 2),  Tocka(1 , 1), Tocka(2 , 1),Tocka(1 , 3),]

#tocke = [ Tocka(-3 , 0),Tocka(-1 , 0), Tocka (-4 , -2), Tocka(-4 , -1),Tocka(-4 , 4),Tocka(0 , -2),]
#tocke = [  Tocka(-1 , 0),Tocka(0 , 0), Tocka(1 , 0),  Tocka(1 , 3),]


#tocke = [Tocka(0,0),Tocka(1,0),Tocka(0,1),Tocka(1,1)]




    # print("GENERIRANE TOČKE: ")
    # for tocka in tocke:
    #     print("\t",tocka)

    tocke = list(set(tocke))
    #tocke = [  Tocka(1 , 3), Tocka(-1 , 0),Tocka(0 , 0), Tocka(1 , 0), ]

    # print("\n'OČIŠĆENE' TOČKE: ")
    # for tocka in tocke:
    #     print("\t",tocka)

for tocka in tocke:
    plt.scatter(tocka.x,tocka.y,color="red")

celije_dijagrama = []

tocke_pom = [i for i in tocke]

# print("\n------------------------------------------------------------------------------------------------")

for trenutna_tocka in tocke_pom:
    # print("\n\tTRENUTNA TOČKA: ",trenutna_tocka)
    tocke.sort(key=lambda tocka: udaljenost_tocke(trenutna_tocka,tocka))

    tocke.pop(0)

    # print("\tSORTIRANE TOČKE: ",tocke)

    rubovi = []

    pronadeno_bar_jedno_sjeciste = False

    for tocka in tocke:
        # print("\n\t*********************************************************************************")

        # print("\n\t\tTOČKA ZA PROVJERU: ",tocka)

        trenutna_duzina = Duzina(trenutna_tocka,tocka)
        trenutna_simetrala = simetrala(trenutna_duzina)

        # print("\t\tTRENUTNA SIMETRALA: ",trenutna_simetrala)

        # print("\n\t\tSVI RUBOVI: ", rubovi,"\n")

        if(len(rubovi)==0):
            rubovi.append(trenutna_simetrala)
            # print("\t\t\tOvo je prvi rub!")
            # print("\t\t\t+ Dodan rub: ",trenutna_simetrala)

        else:
            za_ukloniti =  []

            simetrale_pom = []

            postoji_sjeciste = False

            for postojeci_rub in rubovi:
                # print("\t\t\tPOSTOJEĆI RUB: ",postojeci_rub)
                sjeciste = trenutna_simetrala.sjeciste(postojeci_rub)
                # print("\t\t\tSjecište: ",sjeciste)

                if(not(sjeciste.prazna())):
                    postoji_sjeciste = True
                    pronadeno_bar_jedno_sjeciste = True

                    if(postojeci_rub.A == sjeciste or postojeci_rub.B == sjeciste):
                        tocan_dio_postojeceg_ruba = postojeci_rub

                    else:

                        za_ukloniti.append(postojeci_rub)
                        # print("\t\t\t - Označavanje postojećeg ruba za uklanjanje: ",postojeci_rub)
                        lijeva_polovica_postojeceg_ruba = Duzina(postojeci_rub.A,sjeciste)
                        # print("\n\t\t\tLijeva polovica POSTOJEĆEG RUBA: ",lijeva_polovica_postojeceg_ruba)
                        desna_polovica_postojeceg_ruba = Duzina(postojeci_rub.B,sjeciste)
                        # print("\t\t\tDesna polovica POSTOJEĆEG RUBA: ",desna_polovica_postojeceg_ruba,"\n")

                        tocan_dio_postojeceg_ruba = lijeva_polovica_postojeceg_ruba

                        vektor_do_trenutne_točke = Duzina(sjeciste, trenutna_tocka).u_vektor()

                        kut_između_lpolpostrub_i_vdtt = lijeva_polovica_postojeceg_ruba.u_vektor().kut_izmedu_vektora(vektor_do_trenutne_točke)
                        kut_između_dpolpostrub_i_vdtt = desna_polovica_postojeceg_ruba.u_vektor().kut_izmedu_vektora(vektor_do_trenutne_točke)


                        if(kut_između_lpolpostrub_i_vdtt<kut_između_dpolpostrub_i_vdtt):
                            tocan_dio_postojeceg_ruba = desna_polovica_postojeceg_ruba

                        # print("\t\t\t",kut_između_lpolpostrub_i_vdtt," < ",kut_između_dpolpostrub_i_vdtt,"  =>  ",kut_između_lpolpostrub_i_vdtt<kut_između_dpolpostrub_i_vdtt)

                        simetrale_pom.append(tocan_dio_postojeceg_ruba)
                        # print("\t\t\t+ Dodan rub: ", tocan_dio_postojeceg_ruba)

                    # print("\n\t\t\tTočan dio postojećeg ruba: ",tocan_dio_postojeceg_ruba,"\n")

                    if (trenutna_simetrala.A == sjeciste or trenutna_simetrala.B == sjeciste):
                        tocan_dio_trenutne_simetrale = trenutna_simetrala
                    else:
                        lijeva_polovica_trenutne_simetrale = Duzina(sjeciste, trenutna_simetrala.A)
                        # print("\t\t\tLijeva polovica TRENUTNE simetrale: ", lijeva_polovica_trenutne_simetrale)
                        desna_polovica_trenutna_simetrale = Duzina(sjeciste, trenutna_simetrala.B)
                        # print("\t\t\tDesna polovica TRENUTNE simetrale: ", desna_polovica_trenutna_simetrale)

                        trenutna_tocka_je_na_lijevoj_strani = tocan_dio_postojeceg_ruba.u_vektor().vektorski_produkt(
                            vektor_do_trenutne_točke) > 0

                        # print("\n\t\t\t\tTrenutna točka je na lijevoj strani: ",trenutna_tocka_je_na_lijevoj_strani)

                        lpoltrensim_pripada_poligonu = tocan_dio_postojeceg_ruba.u_vektor().vektorski_produkt(
                            lijeva_polovica_trenutne_simetrale.u_vektor()) > 0

                        # print("\n\t\t\t\tLijeva polovica simetrale pripada poligonu: ",lpoltrensim_pripada_poligonu)

                        if (lpoltrensim_pripada_poligonu == trenutna_tocka_je_na_lijevoj_strani):
                            tocan_dio_trenutne_simetrale = lijeva_polovica_trenutne_simetrale

                        else:
                            tocan_dio_trenutne_simetrale = desna_polovica_trenutna_simetrale


                    # print("\n\t\t\tTočan dio trenutne simetrale: ",tocan_dio_trenutne_simetrale)
                    trenutna_simetrala = tocan_dio_trenutne_simetrale
                    # print("\n\t\t\t\tTrenutna simetrala postaje: ",trenutna_simetrala)
                elif(not pronadeno_bar_jedno_sjeciste):
                    simetrale_pom.append(trenutna_simetrala)
                    # print("\n\t\t\tOva simetrala je paralelna sa svima postojećima!")
                    # print("\t\t\t+ Dodan rub: ", trenutna_simetrala)



            # print("\n\t\tZa ukloniti: ")
            # for duzina in za_ukloniti:
            #     print("\t\t\t",duzina,"\n")

            for sim in za_ukloniti:
                for simica in rubovi:
                    if(simica==sim):
                        rubovi.remove(simica)
                        # print("\t\tUKLANJAM: ",simica)
                        break

            for sim in simetrale_pom:
                rubovi.append(sim)

            if(postoji_sjeciste):
                rubovi.append(trenutna_simetrala)


        # print("\n\t*********************************************************************************")

        # print("\nPRONAĐENI RUBOVI: ")
        # for rub in rubovi:
        #     print("\t",rub)
        # print("----------------------------------")


    # print("\n\t//////////////////////////////////////////////////////////////////////////////////////////////")

    for s1 in rubovi:
        # print("Rub koji provjeravamo: ",s1)
        tocka_je_lijevo = s1.u_vektor().vektorski_produkt(Duzina(s1.B,trenutna_tocka).u_vektor())>0

        # print("Trenutna tokča je na strani: ",tocka_je_lijevo)
        # print("\t---",s1.u_vektor().vektorski_produkt(Duzina(s1.B,trenutna_tocka).u_vektor()))
        for s2 in rubovi:
            # print("\n\tRub za provjeru: ",s2)
            if (not(s2.A == s1.A or s2.A == s1.B)):
                tockaA_je_lijevo = s1.u_vektor().vektorski_produkt(Duzina(s1.B, s2.A).u_vektor())>0
                # print("\n\tTočka A: ",s2.A)
                # print("\tTočka A je na strani: ",tockaA_je_lijevo)
                # print("\t\t--",s1.u_vektor().vektorski_produkt(Duzina(s1.B, s2.A).u_vektor()))
                if(tockaA_je_lijevo!=tocka_je_lijevo):
                    za_ukloniti.append(s2)
                    # print("\t\tUklanjam točku A")
            if (not(s2.B == s1.A or s2.B == s1.B)):
                tockaB_je_lijevo = s1.u_vektor().vektorski_produkt(Duzina(s1.B, s2.B).u_vektor())>0
                # print("\n\tTočka B: ",s2.B)
                # print("\tTočka B je na strani: ",tockaB_je_lijevo)
                # print("\t\t--",s1.u_vektor().vektorski_produkt(Duzina(s1.B, s2.B).u_vektor()))
                if(tockaB_je_lijevo!=tocka_je_lijevo):
                    za_ukloniti.append(s2)
    #                 print("\t\tUklanjam točku B")
    # print("SIMETRALE ZA UKLONITI POSLIJE: ")
    # for zu in za_ukloniti:
    #     print("\t",zu)


    for sim in za_ukloniti:
        for simica in rubovi:
            if(simica==sim):
                # print("ZADNJE UKLANJAM: ",simica)
                rubovi.remove(simica)

    # print("\n\t//////////////////////////////////////////////////////////////////////////////////////////////")

    simetralne_tocke = [tockaa.A for tockaa in rubovi]
    simetralne_tocke += [tockaa.B for tockaa in rubovi if tockaa.B not in simetralne_tocke]

    simetralne_tocke = list(set(simetralne_tocke))

    najmanja = simetralne_tocke[0]


    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


    # for t in simetralne_tocke:
    #     print(t," - ",kut360(Duzina(trenutna_tocka,trenutna_tocka+Tocka(1,0)).u_vektor(),Duzina(trenutna_tocka,t).u_vektor())*57.296)

    simetralne_tocke.sort(key= lambda t: (kut360(Duzina(trenutna_tocka,trenutna_tocka+Tocka(1,0)).u_vektor(),Duzina(trenutna_tocka,t).u_vektor()),Duzina(trenutna_tocka,t).u_vektor().duljina()))

    # for t in simetralne_tocke:
    #     print(t, " - ", kut360(Duzina(trenutna_tocka, trenutna_tocka + Tocka(1, 0)).u_vektor(),
    #                            Duzina(trenutna_tocka, t).u_vektor()) * 57.296)

    # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    voroni_celija = VoronoiCelija(trenutna_tocka,Poligon(simetralne_tocke))

    # print("\n\n DOBIVENA ĆELIJA: ")
    # print("\t TOČKA: ",voroni_celija.Tocka)
    #
    # print("\t POLIGON: ")

    poly = voroni_celija.Poligon.tocke

    # for tocka in poly:
    #     print("\t\t",tocka)

    celije_dijagrama.append(voroni_celija)

    tocke.insert(0,trenutna_tocka)
    # print("\n\n\n\n...................................................................................................................")

# print("------------------------------------------------------------------------------------------------")


color = (0,0,0)
for poligon in celije_dijagrama:

    y = list(color)

    y[0]=random()
    y[1]=random()
    y[2]=random()
    color = tuple(y)

    poligon = poligon.Poligon.u_duzine()

    for simetrala in poligon:
        plt.plot([simetrala.A.x,simetrala.B.x],[simetrala.A.y,simetrala.B.y],color="green")

plt.scatter(trenutna_tocka.x,trenutna_tocka.y,color="blue")
print(" **** T O Č K E : ",tocke," : T O Č K E ****")


# celije_dijagrama.sort(key = lambda nesta: nesta.Tocka.y)
#
# djuzine = []
#
# for i in range(0,len(celije_dijagrama)):
#     for j in range(i+1,len(celije_dijagrama)):
#         for z in range(0,len(celije_dijagrama[i].Poligon.u_duzine())):
#             for k in range(0,len(celije_dijagrama[j].Poligon.u_duzine())):
#                 if(celije_dijagrama[i].Poligon.u_duzine()[z]==celije_dijagrama[j].Poligon.u_duzine()[k]):
#                     djuzine.append(Duzina(celije_dijagrama[i].Tocka,celije_dijagrama[j].Tocka))
#
# for i in range(0,len(djuzine)):
#     plt.plot([djuzine[i].A.x, djuzine[i].B.x], [djuzine[i].A.y, djuzine[i].B.y], color="purple",linestyle="-")


plt.show()


