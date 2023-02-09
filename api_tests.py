from api.oanda_api import OandaApi
from instrumentCollection.instrument_collection import instrumentCollection as ic
import time

#TODO: Make that money!
if __name__ == '__main__':
     api = OandaApi()
     ic.LoadInstruments("./data")
     # trade_id = api.place_trade("GBP_JPY", 100, 1)
     # print("opened:", trade_id)
     # time.sleep(10)
     # print(f"Closing {trade_id}", api.close_trade(trade_id))
     [api.close_trade(x.id) for x in api.get_open_trades()] # type: ignore    