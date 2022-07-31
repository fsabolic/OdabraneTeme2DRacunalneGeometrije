#trebalo bi promijeniti imena u UPPER_CASE

import numpy as np
import matplotlib.pyplot as plt

#koliko "visoko" idu x i y-os
xmin, xmax, ymin, ymax = -10,10,-10,10

#koliko često se prikazuju brojevi na x i y-osi
ticks_frequency = 1

#veličina slike koja će se prikazati (u inčima)
#vraća fig (predstavlja prozor koji prikazuje crtež) i os
fig, ax = plt.subplots(figsize=(12,8))

#postavlja neku boju pozadine
fig.patch.set_facecolor('#ffffff')

#postavljanje limita osi (do kud idu), to je metoda kojom mogu svašta u vezi izgleda grafa mijenjat
ax.set(xlim=(xmin-1, xmax+1), ylim=(ymin-1, ymax+1), aspect='equal')

ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')

#da li da se vide okviri prozora (samo se vide top i right, bottom i left se nikad ne vide)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#postavljanje oznake osi, labelpad govori koliko je oznaka udaljena od osi
ax.set_xlabel('$x$', size=11, labelpad=-24, x=1.02)
ax.set_ylabel('$y$', size=11, labelpad=-21, y=1.02, rotation=0)


plt.text(0.49, 0.49, r"$O$", ha='right', va='top', transform=ax.transAxes, horizontalalignment='center', fontsize=12)

#ovdje napravimo numpy polje svih oznaka na x/y osima, te oznake će stvarno biti na osima
x_ticks = np.arange(xmin, xmax+1, ticks_frequency)
y_ticks = np.arange(ymin, ymax+1, ticks_frequency)

#ovdje stvarno postavimo sve vrijednosti iz onih numpy polja koja smo napravili (osim nule, nulu ne želimo prikazati samo zato što je malo neuredno)
ax.set_xticks(x_ticks[x_ticks != 0])
ax.set_yticks(y_ticks[y_ticks != 0])

#ovdje kažemo da se smiju koristiti minor tickovi (odnosno tickovi između tickova koji imaju oznaku), a ponovo smo poslali numpy polje (sada bez step parametra) tako da se svi tickovi postave
ax.set_xticks(np.arange(xmin, xmax+1), minor=True)
ax.set_yticks(np.arange(ymin, ymax+1), minor=True)

#which - na koje linije se odnosi (na one koje izlaze iz x i y osi)
ax.grid(which='both', color='grey', linewidth=1, linestyle='--', alpha=0.2)