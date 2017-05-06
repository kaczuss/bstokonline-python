import os

if os.getenv('bstok_env') is None:
    os.environ['bstok_env'] = 'test'

print(os.environ['bstok_env'])

from trello_integration import Trello
from offers_finder import OffersFinder
from storage import OffersStorage

storage = OffersStorage()
last_offer_date = storage.find_latest_date()
old_offers = storage.find_all()
# print("latest offer from {}".format(last_offer_date))
finder = OffersFinder()
offers = finder.get_latest_offers(last_offer_date)


def is_new_offer(offer, old_offers):
    for old_offer in old_offers:
        if old_offer['title'] == offer.title:
            return False
    return True


for offer in offers:
    if is_new_offer(offer, old_offers):
        Trello().add_offers([offer])
        storage.store(offer)
    else:
        print('offer already added {}'.format(offer._id))

print("done")
