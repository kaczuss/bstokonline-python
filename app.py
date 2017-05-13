import os
import time

if os.getenv('bstok_env') is None:
    os.environ['bstok_env'] = 'test'

print(os.environ['bstok_env'])

from trello_integration import Trello
from storage import OffersStorage
from offers_finder import OffersFinder


def run():
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
            added_offer = storage.store(offer)
            old_offers.append(added_offer)
            print('offer added {} with title {}'.format(offer._id, offer.title))
        else:
            print('offer already added {} with title {}'.format(offer._id, offer.title))

    print("done")


while True:
    run()
    time.sleep(15 * 60)
