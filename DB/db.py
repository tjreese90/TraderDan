from pymongo import MongoClient, errors

from constants.defs import MONGO_CONN_STR

class DataDB:
    
    SAMPLE_COLL = "forex_sample"
    
    def __init__(self):
        self.client = MongoClient(MONGO_CONN_STR)
        self.db = self.client.Forex_Learning
    
    def test_connection(self):
        print(self.db.list_collection_names())