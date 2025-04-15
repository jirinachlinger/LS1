class Uzivatel:
    def __init__(self, jmeno):
        self.jmeno = jmeno
        self.prevody = []

    def pridej_prevod(self, prevod):
        self.prevody.append(prevod)

    def vypis_prevody(self):
        return [str(p) for p in self.prevody]

