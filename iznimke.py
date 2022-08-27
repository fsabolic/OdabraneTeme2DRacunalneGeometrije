"""Sadrži klase za korisnički definirane iznimke
"""


class IsteKrajnjeTockeError(Exception):
    """Iznimka za dvije iste kranje točke dužine."""

    def __init__(self):
        """

        """
        self.poruka = "Dužina ne može biti zadana dvjema točkama koje su jednake"
        super().__init__(self.poruka)


class PremaloTocakaError(Exception):
    """Iznimka za premalen zadan skup točaka."""

    def __init__(self, poruka):
        """

        """
        self.poruka = poruka
        super().__init__(self.poruka)
