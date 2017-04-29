import json
from datetime import datetime

from trello import TrelloClient
from json import JSONEncoder
import app_config

class MyEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return o.__dict__

def add_offers(offers):

    client = TrelloClient(
        api_key=app_config.API_KEY,
        api_secret=app_config.API_SECRET,
        token=app_config.TOKEN
    )

    board = client.add_board('test2')
    list = board.add_list("nowe")
    for offer in offers:
        list.add_card(offer.title, json.dumps(offer, cls=MyEncoder))


