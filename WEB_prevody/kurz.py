import requests

class KurzFetcher:
    def __init__(self, url):
        self.url = url
    
    def ziskej_kurzy(self):
        try:
            # Posíláme GET request na API ČNB
            response = requests.get(self.url)
            
            # Pokud není odpověď úspěšná (status_code != 200), vyvoláme výjimku
            if response.status_code != 200:
                raise Exception(f"Chyba při stahování dat: {response.status_code}")
            
            # Pokud je odpověď úspěšná, získáme data ve formátu JSON
            data = response.json()

            # Vytvoříme slovník kurzů (přidáme CZK jako základní měnu)
            kurzy = {"CZK": {"rate": 1.0}}  # CZK je základní měna, její kurz je 1

            # Projdeme kurzy z API a přidáme je do slovníku
            for kurz in data["rates"]:
                mena = kurz["code"]
                hodnota = kurz["rate"]
                kurzy[mena] = {"rate": hodnota}
            
            return kurzy

        except Exception as e:
            # Pokud dojde k chybě, vrátíme ji jako zprávu
            print(f"Chyba při stahování kurzů: {e}")
            return None  # Můžeme vrátit None nebo prázdný slovník, podle potřeby