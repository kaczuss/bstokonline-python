from pymongo import MongoClient

import app_config_prod

client = MongoClient(app_config_prod.MONGO_URL)
current_db = client.get_database(app_config_prod.DB_NAME)
target_db = client.get_database('test2')

source = current_db.get_collection('offers')
target = target_db.get_collection('offers')

offers = source.find()
target.insert_many(offers)


