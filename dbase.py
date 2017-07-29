import redis
import time
import apifetch

global database
database = 2


def update_from_website(field):
    """

    Args:
        field

    Returns:
        status
    """
    rd = redis.StrictRedis(host="localhost", port=6379, db=database)
    last_update = rd.get("Last_update_time")
    if last_update["hour"] - time.time().tm_hour < "2":
       return "NO"
    elif field == "category":
        categories = apifetch.fetch_json("http://www.sunbyteit.com:8000/api/", "categories")
        last_update = time.time()
        rd.set("categories", value=categories)
        rd.set("Last_update_time", last_update)
        return "OK"
    elif field == "products":
        products = apifetch.fetch_json("http://www.sunbyteit.com:8000/api/", "categories")
        rd.set("products", values=products)
        return "OK"
    last_update = []
