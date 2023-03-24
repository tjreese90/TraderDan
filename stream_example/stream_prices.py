import json
import requests
from models.live_api_price import LiveApiPrice
from instrumentCollection.log_wrapper import LogWrapper
import constants.defs as defs
import threading
import pandas as pd
from timeit import default_timer as timer

STREAM_URL = f"https://stream-fxpractice.oanda.com/v3/"


class PriceStreamer(threading.Thread):
    # Log every 60 seconds.
    LOG_FREQ = 60
    
    def __init__(self, shared_prices, price_lock: threading.Lock, price_events):
        super().__init__()
        self.pairs_list = shared_prices.keys()
        self.price_lock = price_lock
        self.price_events = price_events
        self.shared_prices = shared_prices
        self.log = LogWrapper("PrintStreamer")
        print(self.pairs_list)
        
    def fire_new_price_event(self, insturment):
        if self.price_events[insturment].is_set() == False:
            self.price_events[insturment].set()

    def updated_live_price(self, live_price: LiveApiPrice):
        try:
            self.price_lock.acquire()
            self.shared_prices[live_price.instrument] = live_price
            self.fire_new_price_event(live_price.instrument)
        except Exception as error:
            self.log.logger.error(f"Exception: {error}")
        finally:
            self.price_lock.release()
            
    def log_data(self):
        self.log.logger.debug("")
        self.log.logger.debug(f"\n{pd.DataFrame.from_dict([v.get_dict() for _, v in self.shared_prices.items()])}") # type: ignore
        
        
    def run(self):
        
        start = timer() - PriceStreamer.LOG_FREQ + 10

        params = dict(
            instruments=','.join(self.pairs_list)
        )

        url = f"{STREAM_URL}accounts/{defs.ACCOUNT_ID}/pricing/stream"

        resp = requests.get(url, params=params,
                            headers=defs.SECURE_HEADER, stream=True)

        for price in resp.iter_lines():
            if price:
                decoded_line = price.decode("utf-8")
                decoded_price = json.loads(decoded_line)
                # print(json.dumps(decoded_price, indent=4), "\n")
                if 'type' in decoded_price and decoded_price['type'] == 'PRICE':
                    self.updated_live_price(LiveApiPrice(decoded_price))
                    if timer() - start > PriceStreamer.LOG_FREQ:
                        print(LiveApiPrice(decoded_price).get_dict())
                        self.log_data()
                        start = timer()
