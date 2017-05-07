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
print("latest offer from {}".format(last_offer_date))
finder = OffersFinder()
offers = finder.get_latest_offers(last_offer_date)


def is_new_offer(new_offer, offers_to_ignore):
    for old_offer in offers_to_ignore:
        if old_offer['title'] == new_offer.title:
            return False
    return True

print('found new {} offers'.format(offers.__len__()))
for offer in offers:
    if is_new_offer(offer, old_offers):
        Trello().add_offers([offer])
        storage.store(offer)
        print('offer added {}'.format(offer._id))
    else:
        print('offer already added {}'.format(offer._id))

print("done")
