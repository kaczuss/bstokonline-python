from offers_finder import OffersFinder
from storage import OffersStorage
from trello_integration import Trello

storage = OffersStorage()
last_offer_date = storage.find_latest_date()

finder = OffersFinder()
offers = finder.get_latest_offers(last_offer_date)

Trello().add_offers(offers)
print("done")
