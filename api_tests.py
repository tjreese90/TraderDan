from api.oanda_api import OandaApi
from instrumentCollection.instrument_collection import instrumentCollection as ic
import time
from models.candle_timing import CandleTiming
import constants.defs as defs
from bot.trade_risk_calculator import get_trade_units


def lm(msg, pair):
     print(msg, pair)

#TODO: Make that money!
if __name__ == '__main__':
     api = OandaApi()
     ic.LoadInstruments("./data")
     # dd = api.last_complete_candle("USD_JPY", granularity="M5")
     # print(CandleTiming(dd))
     # print(api.get_prices(["GBP_JPY", "USD_JPY"]))
     print(get_trade_units(api, "USD_JPY", defs.SELL, 0.4 , 60, lm))
