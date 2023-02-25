import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


from api.oanda_api import OandaApi
from models.trade_settings import TradeSettings


ADD_ROWS = 20

def process_candles(df: pd.DataFrame, pair, trade_settings: TradeSettings, log_message):
    
    df.reset_index(drop=True, inplace=True)
    df['PAIR'] = pair
    df['SPREAD'] = df.ask_c - df.bid_c
    
    # make indicator
    
    log_cols = ['PAIR', 'time', 'mid_c', 'mid_o', 'SPREAD']
    log_message(f"process_candles:\n{df[log_cols].tail()}", pair)

def fetch_candles(pair, row_count, candle_time, granularity, api: OandaApi, log_message):
    
    df = api.get_candles_df(pair, count=row_count, granularity=granularity)
    
    if df is None or df.shape[0] == 0:
        log_message("tech_manger fetch_candles failed to get candles", pair)
        return None
    
    #  you can try to retry to get the candle 3 or 4 times and it sometimes works out.
    if df.iloc[-1].time != candle_time:
        log_message(f"tech_manger fetch_candles {df.iloc[-1].time} not correct", pair)
        return None
    
    return df

def get_trade_decision(candle_time, pair, granularity, api: OandaApi, trade_settings: TradeSettings, log_message):
    
    max_rows = trade_settings.n_ma + ADD_ROWS
    
    log_message(f"tech_manger: max_rows{max_rows} candle_time:{candle_time} granularity:{granularity}", pair)
    
    df = fetch_candles(pair, max_rows, candle_time, granularity, api, log_message)
    
    if df is not None:
        process_candles(df, pair, trade_settings, log_message)
    
    return None