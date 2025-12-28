import requests
from numerize import numerize

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

def game_info(appid:str, currency:str="IN") -> dict:
    # Backup URL: "https://www.protondb.com/proxy/steam/api/appdetails"
    url = "https://store.steampowered.com/api/appdetails"
    params = {
        "appids": appid,
        "cc": currency
    }
    info = dict()
    try:
        res = session.get(url, params=params)
        res.raise_for_status()
        data = res.json()

        d = data[appid].get("data")

        info["product_type"] = d.get("type")
        info["name"] = d.get("name")
        info["steam_appid"] = d.get("steam_appid")
        info["short_description"] = d.get("short_description")
        info["header_image"] = d.get("header_image")
        info["website"] = d.get("website")

        info["pc_requirements"] = d.get("pc_requirements")

        try:
            info["developers"] = d.get("developers")[0]
            info["publishers"] = d.get("publishers")[0]
        except IndexError as err:
            print(f"Error in game info: {err}")
            info["developers"] = None
            info["publishers"] = None

        info["price"] = None
        # print(d.get("price_overview"))

        if d.get("price_overview") is not None:
            try:
                info["price"] = dict()

                init_price = d.get("price_overview").get("initial") // 100
                fin_price = d.get("price_overview").get("final") // 100
                discount = int(((fin_price - init_price) / init_price) * 100)

                init_price = f"{init_price:,}"
                fin_price = f"{fin_price:,}"

                if d.get("price_overview").get("currency") == "INR":
                    info["price"]["currency"] = "₹"

                info["price"]["initial"] = init_price
                info["price"]["final"] = fin_price
                info["price"]["discount"] = discount
            except Exception as err:
                print(f"Error: Price data not available: {err}")

        info["platforms"] = d.get("platforms")
        info["metacritic"] = d.get("metacritic")
        info["genres"] = [g.get("description") for g in d.get("genres")]

        info["screenshots"] = d.get("screenshots")
        info["movies"] = d.get("movies")

        info["release_date"] = d.get("release_date")
        info["background_raw"] = d.get("background_raw")
    except Exception as err:
        print(f"Error in steam game info: {err}")

    return info

def proton_report(appid:str) -> dict:
    url = f"https://www.protondb.com/api/v1/reports/summaries/{appid}.json"
    report = dict()
    try:
        res = session.get(url)
        res.raise_for_status()
        data = res.json()

        report["score"] = data.get("score")
        report["tier"] = data.get("tier")
        report["total"] = data.get("total")
    except Exception as err:
        print(f"Error proton report: {err}")

    return report

def steam_reviews(appid:str, lang:str="english") -> dict:
    url = f"https://store.steampowered.com/appreviews/{appid}"
    params = {
        "json": 1,
        "language": lang,
    }
    user_reviews = dict()
    try:
        res = session.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        # print(data)

        total_positive = int(data["query_summary"]["total_positive"])
        total_reviews = int(data["query_summary"]["total_reviews"])
        positive_percentage = 0.00
        try:
            positive_percentage = round((total_positive / total_reviews) * 100, 2)
        except ZeroDivisionError as err:
            print(f"No reviews found: {err}")

        user_reviews["review_summary"] = {
            "description": data.get("query_summary").get("review_score_desc"),
            "total_reviews": numerize.numerize(total_reviews),
            "total_positive": numerize.numerize(total_positive),
            "positive_percentage": positive_percentage,
        }
        reviews = []
        for rev in data.get("reviews"):
            if len(rev.get("review")) <= 2000:
                r = {
                    "review": rev.get("review"),
                    "timestamp_created": rev.get("timestamp_created"),
                    "voted_up": rev.get("voted_up"),
                    "votes_up": rev.get("votes_up"),
                }
                reviews.append(r)
        user_reviews["reviews"] = [{**rev, "id": i} for i, rev in enumerate(reviews[:10])]
    except Exception as err:
        print(f"Error steam reviews: {err}")

    return user_reviews
