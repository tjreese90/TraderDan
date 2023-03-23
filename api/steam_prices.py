import json
import requests
from models.live_api_price import LiveApiPrice
from instrumentCollection.log_wrapper import LogWrapper
import constants.defs as defs
import threading

STREAM_URL = f"https://stream-fxpractice.oanda.com/v3/"

class PriceStreamer(threading.Thread):
    
    def __init__(self, shared_prices, price_lock: threading.Lock, price_events):
        super().__init__()
        self.pairs_list = shared_prices.keys()
        self.price_lock = price_lock
        self.price_events = price_events
        self.shared_prices = shared_prices
        self.log = LogWrapper("PrintStreamer")
        print(self.pairs_list)    

    def run(self):
        
        
        params = dict(
            instruments=','.join(self.pairs_list)
        )
        
        url = f"{STREAM_URL}accounts/{defs.ACCOUNT_ID}/pricing/stream"
        
        
        resp = requests.get(url, params=params, headers=defs.SECURE_HEADER, stream=True)
        
        for price in resp.iter_lines():
            if price:
                decoded_line = price.decode("utf-8")
                decoded_price = json.loads(decoded_line)
                # print(json.dumps(decoded_price, indent=4), "\n")
                if 'type' in decoded_price and decoded_price['type'] == 'PRICE':
                    print(LiveApiPrice(decoded_price))