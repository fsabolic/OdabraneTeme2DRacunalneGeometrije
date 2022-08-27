from vizualizacije import *


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


generiraj_broj()
sve(100)