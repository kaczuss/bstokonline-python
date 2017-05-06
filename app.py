import os

if os.getenv('bstok_env') is None:
    os.environ['bstok_env'] = 'test'

print(os.environ['bstok_env'])

from trello_integration import Trello
from offers_finder import OffersFinder
from storage import OffersStorage


storage = OffersStorage()
last_offer_date = storage.find_latest_date()
#print("latest offer from {}".format(last_offer_date))
finder = OffersFinder()
offers = finder.get_latest_offers(last_offer_date)

for offer in offers:
    Trello().add_offers([offer])
    storage.store(offer)

print("done")
