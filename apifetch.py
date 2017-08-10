import requests as req
import logging

# from telegbot import logger

# baseurl = "http://sunbyteit.com/"

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='./telegbot.log',
                    format=LOG_FORMAT,
                    filemode='w',
                    level=logging.DEBUG)

logger = logging.getLogger()

def fetch_json(base, route):
    product = req.get(base + route)
    logger.info("a request to the api was sent")
    return product.json()

    reply_markup = build_menu(button_list, n_cols=len(cat_names))
    logger.debug("reply keyboard for category was returned")
