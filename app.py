import os
from utils import fetch, save
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    wishlist = dict()
    wishlist_filepath = "data/wishlist.json"
    is_wishlist_old = save.is_file_old(wishlist_filepath, days=7)

    if is_wishlist_old:
        os.remove(wishlist_filepath)

    if not os.path.isfile(wishlist_filepath):
        wishlist = fetch.wishlist()
        save.write_json(wishlist_filepath, wishlist)
    else:
        wishlist = save.read_json(wishlist_filepath)

    return render_template("index.html", wishlist=wishlist)


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


@app.route("/deals/<int:page_num>")
def deal_page(page_num):
    deals = dict()
    deals_filepath = f"data/deals/{page_num}.json"
    is_deals_old = save.is_file_old(deals_filepath, days=1)

    if is_deals_old:
        os.remove(deals_filepath)

    if not os.path.isfile(deals_filepath):
        deals = fetch.steam_deals(page=page_num-1)
        save.write_json(deals_filepath, deals)
    else:
        deals = save.read_json(deals_filepath)

    return render_template("deals.html", deals=deals, page_num=page_num)

@app.route("/help")
def help():
    return render_template("help.html")

if __name__ == "__main__":
    app.run(port=8080, debug=True, host="0.0.0.0")
