import ssl
import requests
import constants.defs as defs
import pandas as pd
import constants.defs as defs
from dateutil import parser
from datetime import datetime as dt

from models.api_price import ApiPrice
from instrumentCollection.instrument_collection import instrumentCollection as ic
import json

from models.open_trade import OpenTrade


class OandaApi:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization" : f"Bearer {defs.API_KEY}",
            "Content-Type" : "application/json"
        })
    
    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None):
        full_url = f"{defs.URL}/{url}"

        if data is not None:
            data = json.dumps(data)

        try:
            response = None
            if verb == "get":
                response = self.session.get(full_url,params=params, data=data, headers=headers) # type: ignore
            if verb == "post":
                response = self.session.post(full_url,params=params, data=data, headers=headers)

            if verb == "put":
                response = self.session.put(full_url,params=params, data=data, headers=headers)

            if response == None:
                return False, {'error': 'verb request not found'}
            
            if response.status_code == code:
                return True, response.json()
            else:
                return False, response.json()
        except Exception as error:
            return False, {'Exception': error}
    
    def get_account_endPoint(self, ep, data_key):
        url = f"accounts/{defs.ACCOUNT_ID}/{ep}"
        ok, data = self.make_request(url)
        if ok == True and data_key in data:
            return data[data_key]
        else:
            print("Error get_account_ep()", data)
            return None
    
    def get_account_summary(self):
        return self.get_account_endPoint("summary","account")
    
    def get_account_instruments(self):
        return self.get_account_endPoint("instruments","instruments")
    
    def fetch_candles(self,pair_name, count=10, granularity="H1", price="MBA", date_f=None, date_t=None): 
        url = f"/instruments/{pair_name}/candles"
        params = dict(
        granularity = granularity,
        price = price
        )
        
        if date_f is not None and date_t is not None:
            date_format = "%Y-%m-%dT%H:%M:%SZ"
            params["from"] = dt.strftime(date_f, date_format)
            params["to"] = dt.strftime(date_t, date_format)
        else:
            params["count"] = count # type: ignore  
          
        ok, data = self.make_request(url, params=params)       
        if ok == True and 'candles' in data:
            return data['candles']
        else:
            print("Error fetch_candles()", params, data)
            return None

    def get_candles_df(self, pair_name, **kwargs):
        
        data = self.fetch_candles(pair_name, **kwargs)
        
        if len(data) == 0:  # type: ignore
            return pd.DataFrame()
        
        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']
        
        final_data = []
        for candle in data: # type: ignore
            if candle['complete'] == False:
                continue
            new_dict = {}
            new_dict['time'] = parser.parse(candle['time'])
            new_dict['volume'] = candle['volume']
            for p in prices:
                if p in candle:
                    for o in ohlc:
                        new_dict[f"{p}_{o}"] = float(candle[p][o])
            final_data.append(new_dict)
        df = pd.DataFrame.from_dict(final_data) # type: ignore
        return df
    
    def last_complete_candle(self, pair_name, granularity):
        df = self.get_candles_df(pair_name, granularity=granularity, count=10)
        if df.shape[0] == 0:
            return None
        return df.iloc[-1].time
    
    def place_trade(self, pair_name: str, units: float, direction: int, stop_loss: float=None, take_profit: float=None): # type: ignore

        url = f"accounts/{defs.ACCOUNT_ID}/orders"
        instrument = ic.instruments_dict[pair_name]
        units = round(units, instrument.tradeUnitsPrecision)

        if direction == defs.SELL:
            units = units * -1

        data = dict(
            order=dict(
                units=str(units),
                instrument=pair_name,
                type="MARKET"
            )
        )   

        if stop_loss is not None:
            sld = dict(price=str(round(stop_loss, instrument.displayPrecision)))
            data['order']['stopLossOnFill'] = sld  # type: ignore

        if take_profit is not None:
            tpd = dict(price=str(round(take_profit, instrument.displayPrecision)))
            data['order']['takeProfitOnFill'] = tpd  # type: ignore

        # print(data)
        ok, response = self.make_request(url, verb="post", data=data, code=201)
        # print(ok, response)

        if ok == True and 'orderFillTransaction' in response:
            return response['orderFillTransaction']['id'] # type: ignore
        else:
            return None

    def close_trade(self, trade_id):
        url = f"accounts/{defs.ACCOUNT_ID}/trades/{trade_id}/close"
        ok, _ = self.make_request(url, verb="put", code=200)

        if ok == True:
            print(f"Closed {trade_id} succefully")
        else:
            print(f"Failed to close {trade_id}")
    
        return ok
    
    def get_open_trade(self, trade_id):
        url = f"accounts/{defs.ACCOUNT_ID}/trades/{trade_id}"
        ok, response = self.make_request(url)

        if ok == True and 'trade' in response:
            return OpenTrade(response['trade'])


    def get_open_trades(self):
        url = f"accounts/{defs.ACCOUNT_ID}/openTrades"
        ok, response = self.make_request(url)

        if ok == True and 'trades' in response:
            return [OpenTrade(x) for x in response['trades']] # type: ignore
    
    def get_prices(self, instruments_list):
        url = f"accounts/{defs.ACCOUNT_ID}/pricing"
        
        params = dict(
            instruments=','.join(instruments_list)
        )
        
        ok, response = self.make_request(url, params=params)
        
        if ok == True and 'prices' in response:
            return [ApiPrice(x) for x in response['prices']] # type: ignore
        
        return None
        
    # def create_data_file(pair_name, count=10, granularity="H1"):
    #     code, data = fetch_candles(pair_name, count, granularity)
    #     if code != 200:
    #         print("Failed", pair_name, data)
    #    l;
    # 
    # return
    #     if len(data) == 0:
    #         print("No candles", pair_name)
    #     candles_df = get_candles_df(data)
    #     candles_df.to_pickle(f"../data/{pair_name}_{granularity}.pkl")
    #     print(f"{pair_name} {granularity} {candles_df.shape[0]} candles, {candles_df.time.min()} {candles_df.time.max()}")
        
        