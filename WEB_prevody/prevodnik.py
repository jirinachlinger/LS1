class Prevodnik:
    def __init__(self, kurz):
        self.kurz = kurz

    def prevod(self, mnozstvi):
        return mnozstvi * self.kurz.kurz