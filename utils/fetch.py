import requests

def search_results(search_query: str) -> list[dict]:
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

    return search_results

def game_info(appid: str) -> dict:
    url = "https://www.protondb.com/proxy/steam/api/appdetails"
    params = {
        "appids": appid,
    }
    info = dict()

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()  # raises error if request failed
        data = res.json()

        info["product_type"] = data[appid]["data"]["type"]
        info["name"] = data[appid]["data"]["name"]
        info["steam_appid"] = data[appid]["data"]["steam_appid"]
        info["short_description"] = data[appid]["data"]["short_description"]
        info["header_image"] = data[appid]["data"]["header_image"]
        info["website"] = data[appid]["data"]["website"]

        info["pc_requirements"] = data[appid]["data"]["pc_requirements"]
        info["developers"] = data[appid]["data"]["developers"]
        info["publishers"] = data[appid]["data"]["publishers"]
        info["platforms"] = data[appid]["data"]["platforms"]
        info["metacritic"] = data[appid]["data"]["metacritic"]
        info["genres"] = [g["description"] for g in data[appid]["data"]["genres"]]
        info["screenshots"] = data[appid]["data"]["screenshots"]
        info["movies"] = data[appid]["data"]["movies"]
        info["release_date"] = data[appid]["data"]["release_date"]

    except Exception as err:
        print(f"Error: {err}")

    return info
