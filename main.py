from api.oanda_api import OandaApi
from instrumentCollection.instrument_collection import instrumentCollection as ic
from simulation.ma_cross import run_ma_sum
from dateutil import parser
from instrumentCollection.collect_data import run_collection
from simulation.ema_macd_mp import run_ema_macd
from simulation.ema_macd import run_ema_macd

if __name__ == '__main__':
     api = OandaApi()
     ic.LoadInstruments("./data")
     # run_collection(instrumentCollection, api)
     # ic = instrumentCollection() # type: ignore 
     run_ema_macd(ic)

     # instrumentCollection.CreateFile(api.get_account_instruments(), "./data")
     # instrumentCollection.LoadInstruments("./data")
     # instrumentCollection.PrintInstruments()

    
    
    # dfr = parser.parse("2021-04-21T01:00:00Z")
    # dto = parser.parse("2021-04-28T16:00:00Z")
    
    # df_candles = api.get_candles_df("EUR_USD",granularity="H1", date_f=dfr, date_t=dto)
    
    # print(df_candles.head()) # type: ignore
    # print("----------------------------------")
    # print(df_candles.tail()) # type: ignore
    

    
    # # data = api.get_instruments()
    # # [print(x['name']) for x in data] # type: ignore
    
    # # data1 = api.get_account_summary
    # # print(data1)
    # run_ma_sum(curr_list=["USD", "JPY","EUR","AUD"])
