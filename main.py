from api.oanda_api import OandaApi
from instrumentCollection.instrument_collection import instrumentCollection as ic
from stream_example.streamer import run_streamer
from DB.db import DataDB

if __name__ == '__main__':
    #  api = OandaApi()
    #  ic.LoadInstruments("./data")
    #  # steam_prices(['EUR_USD', 'AUD_NZD', 'GBP_JPY'])
    #  run_streamer()
    d = DataDB()
    d.test_connection()