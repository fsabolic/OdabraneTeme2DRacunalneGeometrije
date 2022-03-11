from klase import *
# from random import *
# from konveksnaljuska import *
# p_1=Poligon(konveksna_ljuska([Tocka(int(random()*100%20-10),int(random()*100%20-10)) for i in range(0,int(random()*100%7+3))]))
# p_2=Poligon(konveksna_ljuska([Tocka(int(random()*100%20-10),int(random()*100%20-10)) for i in range(0,int(random()*100%7+3))]))

# p_1 = Poligon(Tocka(0,6),Tocka(1,3),Tocka(3,5),Tocka(2,2),Tocka(4,1),Tocka(7,0),Tocka(1,-1),Tocka(1,-5),Tocka(3,-5),Tocka(-2,-6),Tocka(-3,-4),Tocka(-1,-5),Tocka(-1,-4),Tocka(-7,-2),Tocka(-1,-1),Tocka(-8,0),Tocka(-1,1),Tocka(-8,4),Tocka(-3,3),Tocka(-4,7),Tocka(-1,4)])
# p_2 = Poligon([Tocka(3,3),Tocka(3,5),Tocka(-6,6),Tocka(-8,4),Tocka(3,-2),Tocka(-7,1),Tocka(-9,-1),Tocka(4,-6),Tocka(7,-1),Tocka(8,1),Tocka(6,3) )

#p_1=Poligon([Tocka(-2,-2),Tocka(-4,3),Tocka(0,2),Tocka(2,0)])
#p_2=Poligon([Tocka(-4,0),Tocka(-4,4),Tocka(2,4),Tocka(2,0)])

#p_1=Poligon([Tocka(-5,-3),Tocka(-4,2),Tocka(-3,-6),Tocka(-1,3),Tocka(0,-6),Tocka(2,1),Tocka(3,-6),Tocka(5,2),Tocka(5,-7),Tocka(3,-9),Tocka(3,-7),Tocka(-5,-7)])
#p_2=Poligon([Tocka(-6,-2),Tocka(-7,-3),Tocka(-6,-4), Tocka(6,-4),Tocka(7,-3),Tocka(6,-2)])

def v_razlika(p_1,p_2):
    razlika = p_1-p_2

    ax.fill([i.x for i in p_2.tocke], [i.y for i in p_2.tocke], facecolor="red", edgecolor="red", alpha=0.3)
    ax.fill([i.x for i in p_1.tocke], [i.y for i in p_1.tocke], facecolor="lightblue", edgecolor="blue", alpha=0.3)
    for u in razlika:
        ax.fill([i.x for i in u], [i.y for i in u], facecolor="none", edgecolor="black")
        ax.scatter([i.x for i in u], [i.y for i in u], color="black")
    plt.show()

    return razlika

def v_presjek(p_1,p_2):
    presjek = p_1*p_2

    ax.fill([i.x for i in p_2.tocke], [i.y for i in p_2.tocke], facecolor="blue", edgecolor="none", alpha=0.4)
    ax.fill([i.x for i in p_1.tocke], [i.y for i in p_1.tocke], facecolor="red", edgecolor="none", alpha=0.4)
    for u in presjek:
        ax.fill([i.x for i in u], [i.y for i in u], facecolor="violet", edgecolor="black")
        ax.scatter([i.x for i in u], [i.y for i in u], color="black")
    plt.show()

    return presjek

def v_unija(p_1,p_2):
    unija  = p_1+p_2

    ax.fill([i.x for i in p_1.tocke], [i.y for i in p_1.tocke], facecolor="red", edgecolor="none", alpha=0.3)
    ax.fill([i.x for i in p_2.tocke], [i.y for i in p_2.tocke], facecolor="blue", edgecolor="none", alpha=0.3)

    for u in unija:
        ax.fill([i.x for i in u], [i.y for i in u], facecolor="none", edgecolor="black")

    for u in unija:
        ax.scatter([i.x for i in u], [i.y for i in u], color="black")
    plt.show()

    return unija