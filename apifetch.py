import requests as req

# from telegbot import logger

# baseurl = "http://sunbyteit.com/"


def fetch_json(base, route):
    product = req.get(base + route)
    # logger.info("a request to the api was sent")
    return product.json()

    reply_markup = build_menu(button_list, n_cols=len(cat_names))
    logger.debug("reply keyboard for category was returned")
