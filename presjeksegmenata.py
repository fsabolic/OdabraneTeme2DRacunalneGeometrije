"""Sadrži funkciju za određivanje presjeka skupa dužina.
"""


def presjek_segmenata(duzine):
    """Vraća sjecišta svih dužina iz liste dužina."""
    sjecista = []
    br_duzina = len(duzine)
    for i in range(br_duzina):
        for j in range(i + 1, br_duzina):
            sjec = duzine[i].sjeciste(duzine[j])
            if not sjec.prazna():
                sjecista.append(sjec)
    return sjecista
