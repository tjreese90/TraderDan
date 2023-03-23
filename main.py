from api.oanda_api import OandaApi
from instrumentCollection.instrument_collection import instrumentCollection as ic
from api.steam_prices import steam_prices
from stream_example.streamer import run_streamer


if __name__ == '__main__':
     api = OandaApi()
     ic.LoadInstruments("./data")
     # steam_prices(['EUR_USD', 'AUD_NZD', 'GBP_JPY'])
     run_streamer()