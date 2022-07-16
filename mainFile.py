# from booloperacije import *
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
# def Dac(tocke):
#     if(len(tocke)>3):
#         tocke_l,tocke_d = razdvoji_tocke(tocke)
#         Dac(tocke_l)
#         Dac(tocke_d)
#         print(tocke_l)
#         print(tocke_d)
#         print("---------------------------------------------------------------------")
#     else:
#         return
#
# tocke=[Tocka(random()*1000%20-10,random()*1000%20-10) for i in range(11)]
#
# tocke = list(set(tocke))
# tocke.sort(key=lambda tocka: tocka.x)
#
# tocke_l,tocke_d = razdvoji_tocke(tocke)
#
# ax.scatter([i.x for i in tocke_l], [i.y for i in tocke_l], color="red")
#
# ax.scatter([i.x for i in tocke_d], [i.y for i in tocke_d], color="blue")
#
# Dac(tocke)
#
#
#
# plt.show()
import matplotlib.pyplot as plt
from random import *
from klase import *

a = 0
b = 0

while(a==b):
    a = Tocka(int(random()*1000%6-3),int(random()*1000%6-3))
    b = Tocka(int(random()*1000%6-3),int(random()*1000%6-3))

koeficijent = 0
tocka_prva = Tocka(None,None)
tocka_druga = Tocka(None,None)

if(a.y==b.y):
    tocka_prva = Tocka(a.x/2+b.x/2,100000)
    tocka_druga = Tocka(a.x/2+b.x/2,-100000)

elif(a.x!=b.x):
    koeficijent = -1 / ((b.y-a.y)/(b.x-a.x))
    srediste = a.mnozenje_skalarom(1/2)+b.mnozenje_skalarom(1/2)
    tocka_prva = Tocka(100000,srediste.y+koeficijent*(100000-srediste.x))
    tocka_druga = Tocka(-100000,srediste.y+koeficijent*(-100000-srediste.x))
    plt.scatter(srediste.x,srediste.y,color="blue")

else:
    koeficijent = 0
    srediste = a.mnozenje_skalarom(1/2)+b.mnozenje_skalarom(1/2)
    tocka_prva = Tocka(100000,srediste.y+koeficijent*(100000-srediste.x))
    tocka_druga = Tocka(-100000,srediste.y+koeficijent*(-100000-srediste.x))
    plt.scatter(srediste.x,srediste.y,color="blue")


d1 = Duzina(a,b)
d2 = Duzina(tocka_prva,tocka_druga)

print(d1.u_vektor().kut_izmedu_vektora(d2.u_vektor())*57.2958)

plt.plot([d1.A.x,d1.B.x],[d1.A.y,d1.B.y], marker = 'o',color="purple")
plt.plot([d2.A.x,d2.B.x],[d2.A.y,d2.B.y], marker = 'o',color="purple")

plt.scatter(a.x,a.y,color="red")
plt.scatter(b.x,b.y,color="red")
plt.scatter(tocka_prva.x,tocka_prva.y,color="blue")
plt.scatter(tocka_druga.x,tocka_druga.y,color="blue")
plt.show()



