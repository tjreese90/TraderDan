from bs4 import BeautifulSoup
import pandas as pd
import requests

def dailyfx_com():
    
    resp = requests.get('https://www.dailyfx.com/sentiment')
    
    # print(resp.content)
    # print(resp.status_code)
    
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    # print(soup.find_all('span', class_='foo'))
    
    rows = soup.select(".dfx-technicalSentimentCard")
    
    
    for r in rows:
        card = r.select_one(".dfx-technicalSentimentCard_pairAndSignal")
        if card is not None:
            pair = card.select_one('a')
            if pair is not None:
                pair_text = pair.text.replace("/", "_")
                print(pair_text)
            else:
                print("Pair is None")

            signal = card.select_one('span')
            if signal is not None:
                signal_text = signal.text
                print(signal_text)
            else:
                print("Signal is None")
        else:
            print("Card is None")


            