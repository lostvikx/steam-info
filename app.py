import os
from utils import fetch, save
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    wishlist = dict()
    deals = dict()
    wishlist_filepath = "data/wishlist.json"
    deals_filepath = "data/deals.json"

    is_wishlist_old = save.is_file_old(wishlist_filepath, days=7)
    is_deals_old = save.is_file_old(deals_filepath, days=1)

    if is_wishlist_old:
        os.remove(wishlist_filepath)
    if is_deals_old:
        os.remove(deals_filepath)

    if not os.path.isfile(wishlist_filepath):
        wishlist = fetch.wishlist()
        save.write_json(wishlist_filepath, wishlist)
    else:
        wishlist = save.read_json(wishlist_filepath)

    if not os.path.isfile(deals_filepath):
        deals = fetch.steam_deals()
        save.write_json(deals_filepath, deals)
    else:
        deals = save.read_json(deals_filepath)

    return render_template("index.html", wishlist=wishlist, deals=deals)


@app.route("/search")
def search():
    search_query = request.args.get("q", "")
    search_results = fetch.search_results(search_query)

    return render_template("search.html", search_query=search_query, search_results=search_results)


@app.route("/game/<string:appid>")
def game_page(appid):
    game = dict()
    game_filepath = f"data/games/{appid}.json"

    is_gamedata_old = save.is_file_old(game_filepath, days=1)
    if is_gamedata_old:
        os.remove(game_filepath)

    if not os.path.isfile(game_filepath):
        game_info = fetch.game_info(appid)
        proton_report = fetch.proton_report(appid)
        reviews = fetch.steam_reviews(appid)
        game = {**game_info, **proton_report, **reviews}
        save.write_json(game_filepath, game)
    else:
        game = save.read_json(game_filepath)

    return render_template("game.html", game=game)


if __name__ == "__main__":
    app.run(port=8080, debug=True, host="0.0.0.0")
