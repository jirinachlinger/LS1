import json
import os

class Uloziste:
    def __init__(self, soubor):
        self.soubor = soubor

    def uloz_data(self, data):
        with open(self.soubor, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def nacti_data(self):
        if os.path.exists(self.soubor):
            with open(self.soubor, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
        
