import requests

class KurzFetcher:
    def __init__(self, url):
        self.url = url

    def ziskej_kurzy(self):
        try:
            response = requests.get(self.url)

            if response.status_code == 200:
                data = response.json()

                kurzy = {
                    "CZK": {"rate": 1.0}  # Základní měna
                }

                for item in data:
                    mena = item["code"]
                    kurz = float(item["rate"])
                    kurzy[mena] = {"rate": kurz}

                return kurzy
            else:
                print(f"Chyba při stahování dat: {response.status_code}")
                return None
        except Exception as e:
            print(f"Výjimka při stahování kurzů: {e}")
            return None