class IsteKrajnjeTockeError(Exception):

    def __init__(self):
        self.poruka = "Dužina ne može biti zadana dvjema točkama koje su jednake"
        super().__init__(self.poruka)


class PremaloTocakaError(Exception):
    def __init__(self, poruka):
        self.poruka = poruka
        super().__init__(self.poruka)
