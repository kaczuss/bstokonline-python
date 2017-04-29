from pymongo import MongoClient
from pymongo.collation import Collation

import app_config

client = MongoClient(app_config.MONGO_URL)
db = client.test
collection = db.create_collection('contacts', collation=Collation(locale='pl'))
