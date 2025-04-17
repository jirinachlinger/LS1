from flask import Flask, render_template, request, jsonify, redirect, url_for
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
    kurzy = kurz_fetcher.ziskej_kurzy()

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

    uloziste = Uloziste("prevody.json")
    prevody = uloziste.nacti_data()

    # Získání aktuálních kurzů
    kurzy = kurz_fetcher.ziskej_kurzy()
    if not kurzy:
        kurzy = {}  # Ošetření, aby kurzy nebyly None

    return render_template("index.html", prevody=prevody, kurzy=kurzy)


@app.route("/convert", methods=["GET"])
def convert():
    amount = float(request.args.get('amount'))
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')

    kurzy = kurz_fetcher.ziskej_kurzy()  # Získej aktuální kurzy
    
    if from_currency in kurzy and to_currency in kurzy:
        rate_from = kurzy[from_currency]["rate"]
        rate_to = kurzy[to_currency]["rate"]
        result = (amount / rate_from) * rate_to
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Invalid currencies"}), 400
    
@app.route("/get_currencies", methods=["GET"])
def get_currencies():
    kurzy = kurz_fetcher.ziskej_kurzy()  # Předpokládám, že kurz_fetcher ti vrátí slovník měn
    currencies = list(kurzy.keys())  # Vytvoří seznam kódů měn
    return jsonify({"currencies": currencies})


if __name__ == "__main__":
    app.run(debug=True)