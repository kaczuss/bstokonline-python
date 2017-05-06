import importlib
import os
from datetime import datetime, timedelta

import pymongo
from json import JSONEncoder
from pymongo import MongoClient

app_config = importlib.import_module('app_config_{}'.format(os.getenv('bstok_env')))


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
        result = collection.insert_one({
            '_id' : offer._id,
            'creation_date' : offer.creation_date,
            'premium' : offer.premium,
            'url' : offer.url,
            'title' : offer.title,
            'user' : offer.user,
            'description' : offer.description,
            'extra_url' : offer.extra_url,
            'price' : offer.price
        })

        print("saved in mongo {}".format(result))


    def __get_collection(self):
        collection = self.db.get_collection(app_config.COLLECTION_NAME)
        return collection

    def find_latest_date(self):
        collection = self.__get_collection()
        result = collection.find().sort("creation_date", pymongo.DESCENDING).limit(1)
        count = result.count()
        if count > 0:
            return result.next()['creation_date']
        return datetime.now() - timedelta(days=7)

