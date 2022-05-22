from pymongo import MongoClient
from db.configs import mongo

client = MongoClient(mongo.config['endpoint'])
db = client.more
