import importlib

from trello import TrelloClient
import os

app_config = importlib.import_module('app_config_{}'.format(os.getenv('bstok_env')))

LIST_NEW_OFFERS = "nowe"


class Trello(object):
    def __init__(self) -> None:
        self.client = TrelloClient(
            api_key=app_config.API_KEY,
            api_secret=app_config.API_SECRET,
            token=app_config.TOKEN
        )
        self.boardName = app_config.BOARD_NAME

    def add_offers(self, offers):
        board = self.get_board()

        cards = self.get_list(board)
        for offer in offers:
            title = offer.title
            if offer.premium:
                title = "[PREMIUM]" + offer.title
            if offer.price:
                title = "[{}]{}".format(offer.price, title)
            cards.add_card(title,
                           "link: {}\nlink2: {}\n\n{}\ntworca: {}\nUtworzony: {}".format(offer.url, offer.extra_url,
                                                                                         offer.description,
                                                                                         offer.user,
                                                                                         offer.creation_date))
            print("added card {}".format(title))

    def get_list(self, board):
        lists = board.list_lists()
        for offers_list in lists:
            if offers_list.name == LIST_NEW_OFFERS:
                return offers_list

        return board.add_list(LIST_NEW_OFFERS)

    def get_board(self):
        boards = self.client.list_boards()

        for b in boards:
            if b.name == self.boardName:
                return b

        return self.client.add_board(self.boardName)
