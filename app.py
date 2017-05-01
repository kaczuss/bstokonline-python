from offers_finder import OffersFinder
from storage import OffersStorage
from trello_integration import Trello

storage = OffersStorage()
last_offer_date = storage.find_latest_date()
print("latest offer from {}".format(last_offer_date))
finder = OffersFinder()
offers = finder.get_latest_offers(last_offer_date)

for offer in offers:
    Trello().add_offers([offer])
    storage.store(offer)

print("done")
