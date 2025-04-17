from flask import Flask, render_template, request, redirect, url_for
from uzivatel import Uzivatel
from prevod import Prevod
from kurz import KurzFetcher
from uloziste import Uloziste

app = Flask(__name__)

# URL pro získání kurzů z API ČNB
url_api = "https://api.cnb.cz/cnbapi/exrates/daily?lang=EN"
kurz_fetcher = KurzFetcher(url_api)

@app.route("/", methods=["GET", "POST"])
def index():
    # Získání aktuálních kurzů
    kurzy = kurz_fetcher.ziskej_kurzy()
    if not kurzy:
        kurzy = {}

    if request.method == "POST":
        mnozstvi = float(request.form["mnozstvi"])
        z_meny = request.form["z_meny"]
        do_meny = request.form["do_meny"]

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

    # Načtení uložených převodů
    uloziste = Uloziste("prevody.json")
    prevody = uloziste.nacti_data()

    return render_template("index.html", prevody=prevody, kurzy=kurzy)

if __name__ == "__main__":
    app.run(debug=True)