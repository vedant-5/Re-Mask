mongodb_url = 'mongodb://127.0.0.1:27017/'
mongodb_name = 'Remask'
from pymongo import MongoClient

def mongodb_connection(collection: str):
    client = MongoClient(mongodb_url)
    database = client[mongodb_name]
    collection = database[collection]
    return collection