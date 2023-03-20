import json
import requests

import constants.defs as defs

STREAM_URL = f"https://stream-fxpractice.oanda.com/v3/"

def steam_prices(pairs_list):
    
    
    params = dict(
        instruments=','.join(pairs_list)
    )
    
    url = f"{STREAM_URL}accounts/{defs.ACCOUNT_ID}/pricing/stream"
    
     
    resp = requests.get(url, params=params, headers=defs.SECURE_HEADER, stream=True)
    
    for price in resp.iter_lines():
        if price:
            decoded_line = price.decode("utf-8")
            decoded_price = json.loads(decoded_line)
            print(json.dumps(decoded_price, indent=4), "\n")
           