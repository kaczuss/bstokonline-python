import importlib
import os
from datetime import datetime, timedelta

import pymongo
from json import JSONEncoder
from pymongo import MongoClient

app_config = importlib.import_module('app_config_{}'.format(os.getenv('bstok_env')))

days_to_check = getattr(app_config, "DAYS_TO_CHECK", 7)
ignore_last_offer_date = getattr(app_config, "IGNORE_LAST_OFFER_DATE", False)


class OfferEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return o.__dict__


class OffersStorage(object):
    def __init__(self) -> None:
        client = MongoClient(app_config.MONGO_URL)
        self.db = client.get_database(app_config.DB_NAME)

    def store(self, offer):
        collection = self.__get_collection()
        offer_to_insert = {'_id': offer._id,
                           'creation_date': offer.creation_date,
                           'premium': offer.premium,
                           'url': offer.url,
                           'title': offer.title,
                           'user': offer.user,
                           'description': offer.description,
                           'extra_url': offer.extra_url,
                           'price': offer.price}
        result = collection.insert_one(offer_to_insert)

        print("saved in mongo {}".format(result))
        return offer_to_insert

    def __get_collection(self):
        collection = self.db.get_collection(app_config.COLLECTION_NAME)
        return collection

    def find_latest_date(self):
        if not ignore_last_offer_date:
            collection = self.__get_collection()
            result = collection.find().sort("creation_date", pymongo.DESCENDING).limit(1)
            count = result.count()
            if count > 0:
                return result.next()['creation_date']

        return datetime.now() - timedelta(days=days_to_check)

    def find_all(self):
        collection = self.__get_collection()
        return list(collection.find().sort("creation_date", pymongo.DESCENDING))
