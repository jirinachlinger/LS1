import requests

class KurzFetcher:
    def __init__(self, url):
        self.url = url
    
    def ziskej_kurzy(self):
        # Posíláme GET request na API ČNB
        response = requests.get(self.url)
        
        if response.status_code != 200:
            raise Exception(f"Chyba při stahování dat: {response.status_code}")
        
        # Získáme data ve formátu JSON
        data = response.json()
        
        # Vytvoříme slovník kurzů
        kurzy = {}
        
        # Předpokládejme, že API vrací seznam kurzů pod klíčem "items"
        for kurz in data["items"]:
            mena = kurz["currency"]
            kurzova_hodnota = kurz["rate"]
            kurzy[mena] = {
                "rate": kurzova_hodnota
            }
        
        return kurzy