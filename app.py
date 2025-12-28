from utils import fetch
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    search_query = request.args.get("q", "")
    search_results = fetch.search_results(search_query)

    return render_template("search.html", search_query=search_query, search_results=search_results)


@app.route("/game/<string:appid>")
def game_page(appid):

    game_info = fetch.game_info(appid)
    proton_report = fetch.proton_report(appid)
    reviews = fetch.steam_reviews(appid)
    merged_game_info = {**game_info, **proton_report, **reviews}

    return render_template("game.html", game=merged_game_info)


if __name__ == "__main__":
    app.run(port=8080, debug=True, host="0.0.0.0")
