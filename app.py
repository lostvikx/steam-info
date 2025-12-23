import os
import json
from flask import Flask, render_template, request
# from fetch import fetch_search_results, fetch_game_info
from utils import fetch

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    search_query = request.args.get("q", "")

    data_path = "data/search_data.json"
    if os.path.isfile(data_path):
        with open(data_path, "r") as f:
            search_results = json.load(f)
        return render_template("search.html", search_query=search_query, search_results=search_results)

    search_results = fetch.search_results(search_query)

    with open(data_path, "w") as f:
        json.dump(search_results, f, indent=4)
    return render_template("search.html", search_query=search_query, search_results=search_results)


@app.route("/game/<int:appid>")
def game_page(appid):

    data_path = f"data/{appid}.json"
    if os.path.isfile(data_path):
        with open(data_path, "r") as f:
            game_info = json.load(f)
            return render_template("game.html", appid=appid, game_info=game_info)

    game_info = fetch.game_info(str(appid))

    with open(data_path, "w") as f:
        json.dump(game_info, f, indent=4)

    return render_template("game.html", appid=appid, game_info=game_info)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
