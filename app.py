import os
import json
from flask import Flask, render_template, request
from time import sleep

from utils import fetch

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    search_query = request.args.get("q", "")

    # data_path = "data/search_data.json"
    # if os.path.isfile(data_path):
    #     with open(data_path, "r") as f:
    #         search_results = json.load(f)
    #     return render_template("search.html", search_query=search_query, search_results=search_results)

    search_results = fetch.search_results(search_query)

    # with open(data_path, "w") as f:
    #     json.dump(search_results, f, indent=4)
    return render_template("search.html", search_query=search_query, search_results=search_results)


@app.route("/game/<string:appid>")
def game_page(appid):

    data_path = f"data/{appid}.json"
    if os.path.isfile(data_path):
        with open(data_path, "r") as f:
            merged_game_info = json.load(f)
            return render_template("game.html", game=merged_game_info)

    game_info = fetch.game_info(appid)
    proton_report = fetch.proton_report(appid)
    reviews = fetch.steam_reviews(appid)

    merged_game_info = {**game_info, **proton_report, **reviews}

    with open(data_path, "w") as f:
        json.dump(merged_game_info, f, indent=4)

    return render_template("game.html", game=merged_game_info)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
