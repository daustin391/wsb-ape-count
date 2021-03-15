""" api services for wsb ape count
this module connects to fcsapi and creates a json file containing a list of stock symbols
"""

import json
import requests
from credentials import FCS_KEY

EXCHANGES = "tsxv,toronto,nyse,nasdaq,neo"


def generate_stock_list():
    """ writes json file containing list of stock symbols """
    stonks = json.loads(
        requests.get(
            "https://fcsapi.com/api-v3/stock/list?exchange="
            + EXCHANGES
            + "&access_key="
            + FCS_KEY
        ).text
    )

    stonks_list = {
        "stonks": [],
    }

    stonks_list["download_time"] = stonks["info"]["server_time"]
    for stonk in stonks["response"]:
        stonks_list["stonks"].append(stonks["response"][stonk]["short_name"])

    with open("stonks.json", "w") as write_file:
        json.dump(stonks_list, write_file)
