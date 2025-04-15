from datetime import datetime

class Prevod:
    def __init__(self, z_meny, do_meny, mnozstvi, kurz):
        if mnozstvi <= 0 or kurz <= 0:
            raise ValueError("Množství a kurz musí být kladné číslo.")
        self.z_meny = z_meny
        self.do_meny = do_meny
        self.mnozstvi = mnozstvi
        self.kurz = kurz
        self.vysledek = round(mnozstvi * kurz, 2)
        self.cas = datetime.now().isoformat()