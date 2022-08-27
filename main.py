import klase
from vizualizacije import *
from klase import *
from presjeksegmenata import *
from konveksnaljuska import  *
from triangulacija import *
from voronoi import *
from iznimke import *

def sve(broj):
    v_presjek_segmenata_test(broj)
    v_tocka_u_poligonu_test(broj)
    v_tocka_u_poligonu_wn_test(broj)
    v_konveksna_ljuska_test(broj)
    v_unija_test()
    v_razlika_test()
    v_presjek_test()
    v_triangulacija_test(broj)
    v_voronoi_test(broj)
    v_triangulacija_voronoi_test(broj)



sve(100)