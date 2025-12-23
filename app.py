import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    search_query = request.args.get("q", "")

    url = "https://store.steampowered.com/api/storesearch/"
    params = {
        "term": search_query,
        "l": "english",
        "cc": "IN",
    }

    search_results = list()

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()  # raises error if request failed

        data = res.json()
        for item in data["items"]:
            game = dict(
                name=item.get("name"),
                id=item.get("id"),
                price=item.get("price"),
                tiny_img=item.get("tiny_image"),
                platforms=item.get("platforms"),
            )

            init_price = game["price"]["initial"] // 100
            fin_price = game["price"]["final"] // 100
            game["price"]["discount"] = int(((fin_price - init_price) / init_price) * 100)

            game["price"]["initial"] = f"{init_price:,}"
            game["price"]["final"] = f"{fin_price:,}"

            if game["price"]["currency"] == "INR":
                game["price"]["currency"] = "₹"

            search_results.append(game)
    except Exception as err:
        print(f"Error: {err}")

    return render_template("search.html", search_query=search_query, search_results=search_results)

@app.route("/game/<int:appid>")
def game_page(appid):
    return render_template("game.html", appid=appid)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
