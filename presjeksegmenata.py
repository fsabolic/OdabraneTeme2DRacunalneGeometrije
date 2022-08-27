"""Sadrži funkciju za određivanje presjeka skupa dužina.
"""


def presjek_segmenata(duzine):
    """

    """
    sjecista=[]
    br_duzina=len(duzine)
    for i in range(br_duzina):
        for j in range(i + 1, br_duzina):
            S = duzine[i].sjeciste(duzine[j])
            if (not S.prazna()):
                sjecista.append(S)
    return sjecista


