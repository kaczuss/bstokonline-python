from datetime import datetime, timedelta

import pymongo
from pymongo import MongoClient
from pymongo.collation import Collation

import app_config

class OffersStorage(object):
    def __init__(self) -> None:
        client = MongoClient(app_config.MONGO_URL)
        self.db = client.get_database(app_config.DB_NAME)

    def store(self, offers):
        collection = self.__get_collection()
        collection.insert_many(offers, ordered=False)

    def __get_collection(self):
        collection = self.db.get_collection('contacts')
        return collection

    def find_latest_date(self):
        # collection = self.__get_collection()
        # result = collection.find().sort("created_date", pymongo.DESCENDING).limit(1)
        # count = result.count()
        # if count > 0:
        #     return result.next().created_date
        return datetime.now() - timedelta(days=14)

