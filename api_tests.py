from api.oanda_api import OandaApi
from instrumentCollection.instrument_collection import instrumentCollection as ic
import time

#TODO: Make that money!
if __name__ == '__main__':
     api = OandaApi()
     ic.LoadInstruments("./data")
     print(api.last_complete_candle("USD_JPY", granularity="M5"))