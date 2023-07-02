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
     api = OandaApi()
    #  ic.CreateDB(api.get_account_instruments())
    # Returns a List of instruments pairs object with data
    #  ic.LoadInstrumentsDB()
    #  print(ic.instruments_dict)
     
     # We added this into run_streamer logic it looks like
     # steam_prices(['EUR_USD', 'AUD_NZD', 'GBP_JPY'])
    # NOTE: run_stream() may only run during OANDA Market Hours
    #  run_streamer()
    # NOTE: We are connecting to the mongoDB here and fetching data we have stored.
     d = DataDB()
     # Return the columns from our data base could have better names
     d.test_connection()
     db_test()