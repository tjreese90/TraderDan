from api.oanda_api import OandaApi
from instrumentCollection.instrument_collection import instrumentCollection as ic
import time
from models.candle_timing import CandleTiming

#TODO: Make that money!
if __name__ == '__main__':
     api = OandaApi()
     ic.LoadInstruments("./data")
     dd = api.last_complete_candle("USD_JPY", granularity="M5")
     print(CandleTiming(dd))