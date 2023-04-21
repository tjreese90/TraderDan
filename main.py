from api.oanda_api import OandaApi
from instrumentCollection.instrument_collection import instrumentCollection as ic
from stream_example.streamer import run_streamer
from DB.db import DataDB

def db_test():
    d = DataDB()
    
    print(d.query_distinct(DataDB.SAMPLE_COLL, "age"))
    
    # data = [
    #     dict(age=12, name='unlceSam', street="elm"),
    #     dict(age=72, name='jale', eyes='purple'),
    #     dict(age=42, name='hobert', eyes='green'),
    #     dict(age=22, name='yace', eyes='yellow'),
    #     dict(age=14, name='Ace', eyes='blue')
    # ]
    
    # d.add_many(DataDB.SAMPLE_COLL, data) 
    # d.add_one(DataDB.SAMPLE_COLL,  dict(age=12, name='unlceSam', street="elm"))

if __name__ == '__main__':
    #  api = OandaApi()
    #  ic.LoadInstruments("./data")
    #  # steam_prices(['EUR_USD', 'AUD_NZD', 'GBP_JPY'])
    #  run_streamer()
    d = DataDB()
    d.test_connection()
    db_test()