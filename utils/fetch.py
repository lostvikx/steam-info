import requests

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
})

def search_results(search_query:str, lang:str="english", currency:str="IN") -> list[dict]:
    url = "https://store.steampowered.com/api/storesearch"
    params = {
        "term": search_query,
        "l": lang,
        "cc": currency,
    }
    search_results = list()
    try:
        res = session.get(url, params=params)
        res.raise_for_status()

        data = res.json()
        for item in data["items"]:
            game = dict(
                name=item.get("name"),
                id=item.get("id"),
                price=item.get("price"),
                tiny_img=item.get("tiny_image"),
                platforms=item.get("platforms"),
            )

            if game.get("price") is None:
                search_results.append(game)
                continue

            init_price = game["price"]["initial"] // 100
            fin_price = game["price"]["final"] // 100
            game["price"]["discount"] = int(((fin_price - init_price) / init_price) * 100)

            game["price"]["initial"] = f"{init_price:,}"
            game["price"]["final"] = f"{fin_price:,}"

            if game["price"]["currency"] == "INR":
                game["price"]["currency"] = "₹"

            search_results.append(game)
    except Exception as err:
        print(f"Error in search: {err}")

    return search_results

def game_info(appid: str) -> dict:
    # Backup URL: "https://www.protondb.com/proxy/steam/api/appdetails"
    url = "https://store.steampowered.com/api/appdetails"
    params = {
        "appids": appid,
    }
    info = dict()
    try:
        res = session.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        d = data[appid].get("data")

        info["product_type"] = d["type"]
        info["name"] = d["name"]
        info["steam_appid"] = d["steam_appid"]
        info["short_description"] = d["short_description"]
        info["header_image"] = d["header_image"]
        info["website"] = d["website"]

        info["pc_requirements"] = d["pc_requirements"]
        info["developers"] = d["developers"]
        info["publishers"] = d["publishers"]

        info["price"] = {
            "currency": d["price_overview"]["currency"],
            "initial": d["price_overview"]["initial"],
            "final": d["price_overview"]["final"],
        }

        info["platforms"] = d["platforms"]
        info["metacritic"] = d["metacritic"]
        info["genres"] = [g["description"] for g in d["genres"]]

        info["screenshots"] = d["screenshots"]
        info["movies"] = d["movies"]

        info["release_date"] = d["release_date"]
        info["background_raw"] = d["background_raw"]
    except Exception as err:
        print(f"Error in steam game info: {err}")

    return info

def proton_report(appid: str) -> dict:
    url = f"https://www.protondb.com/api/v1/reports/summaries/{appid}.json"
    report = dict()
    try:
        res = session.get(url)
        res.raise_for_status()
        data = res.json()

        report["score"] = data["score"]
        report["tier"] = data["tier"]
        report["total"] = data["total"]
    except Exception as err:
        print(f"Error proton report: {err}")

    return report

def steam_reviews(appid: str, filter:str="toprated", num_per_page:int=20, lang:str="english") -> dict:
    url = f"https://store.steampowered.com/appreviews/{appid}"
    params = {
        "json": 1,
        "language": lang,
    }
    reviews = dict()
    try:
        res = session.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        reviews["review_summary"] = {
            "description": data["query_summary"]["review_score_desc"],
            "total_positive": data["query_summary"]["total_positive"],
            "total_negative": data["query_summary"]["total_negative"],
            "total_reviews": data["query_summary"]["total_reviews"]
        }
        reviews["reviews"] = data["reviews"]
    except Exception as err:
        print(f"Error steam reviews: {err}")

    return reviews
