from flask import Flask, render_template, request, redirect, url_for
from uzivatel import Uzivatel
from prevod import Prevod
from prevodnik import Prevodnik
from kurz import KurzFetcher
from uloziste import Uloziste


app = Flask(__name__)

# URL pro získání kurzů z API ČNB
url_api = "https://api.cnb.cz/api/v1/currencies"
kurz_fetcher = KurzFetcher(url_api)  # Inicializuj třídu KurzFetcher

# Cesta pro hlavní stránku
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Získání dat z formuláře
        mnozstvi = float(request.form["mnozstvi"])
        z_meny = request.form["z_meny"]
        do_meny = request.form["do_meny"]
        
        # Načti aktuální kurzy
        kurzy = kurz_fetcher.ziskej_kurzy()
        
        if z_meny in kurzy and do_meny in kurzy:
            kurz = kurzy[do_meny]["rate"] / kurzy[z_meny]["rate"]
            
           
            uzivatel = Uzivatel("Jan")
            prevod = Prevod(z_meny, do_meny, mnozstvi, kurz)
            uzivatel.pridej_prevod(prevod)

            
            uloziste = Uloziste("prevody.json")
            uloziste.uloz_data([str(p) for p in uzivatel.prevody])
            
            
            return redirect(url_for('index'))
        else:

            return "Chyba: Měna nebyla nalezena v aktuálních kurzech."

    uloziste = Uloziste("prevody.json")
    prevody = uloziste.nacti_data()

    return render_template("index.html", prevody=prevody)

if __name__ == "__main__":
    app.run(debug=True)