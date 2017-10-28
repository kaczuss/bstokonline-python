import importlib
import re

import os

if os.getenv('bstok_env') is None:
    os.environ['bstok_env'] = 'test'

print(os.environ['bstok_env'])

from trello_integration import Trello
from storage import OffersStorage
from offers_finder import OffersFinder

app_config = importlib.import_module('app_config_{}'.format(os.getenv('bstok_env')))

max_price = getattr(app_config, 'MAX_PRICE', 400 * 1000)

def parse_price(price):
    if price is None:
        return 0
    price = re.sub(" |zl|zł", '', price, flags=re.IGNORECASE)
    if price.__len__() > 0 and price.isdigit():
        return int(price)
    return 0


def filtered_words(offer):
    forbidden_words = getattr(app_config, 'FORBIDDEN_WORDS', [])

    for word in forbidden_words:
        if check_word(offer, " " + word + "."):
            return True
        if check_word(offer, " " + word + ","):
            return True
        if check_word(offer, " " + word + "/"):
            return True
        if check_word(offer, " " + word + " "):
            return True
        if word.__len__() > 4:
            if check_word(offer, word + " "):
                return True

    return False


def check_word(offer, word):
    if word in offer.title.lower():
        print('forbidden word in title is {}'.format(word))
        return True
    if word in offer.description.lower():
        print('forbidden word in description is {}'.format(word))
        return True
    return False


def filter_price(offer):
    price = parse_price(offer.price)
    return price > 400 * 1000


def is_new_offer(new_offer, offers_to_ignore):
    for old_offer in offers_to_ignore:
        if old_offer['title'] == new_offer.title:
            return False
    return True


def run():
    storage = OffersStorage()
    last_offer_date = storage.find_latest_date()
    old_offers = storage.find_all()
    print("latest offer from {}".format(last_offer_date))
    finder = OffersFinder()
    offers = finder.get_latest_offers(last_offer_date)

    print('found new {} offers'.format(offers.__len__()))
    for offer in offers:
        if not is_new_offer(offer, old_offers):
            print('offer already added {} with title {}'.format(offer._id, offer.title))
        elif filtered_words(offer):
            print('offer {} was filtered with title {}'.format(offer._id, offer.title))
        elif filter_price(offer):
            print('offer {} was filtered with title {} because of price {}'.format(offer._id, offer.title, offer.price))
        else:
            Trello().add_offers([offer])
            added_offer = storage.store(offer)
            old_offers.append(added_offer)
            print('offer added {} with title {}'.format(offer._id, offer.title))

    print("done")
