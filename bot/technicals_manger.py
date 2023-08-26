import constants.defs as defs
from models.trade_settings import TradeSettings
from technicals.indicators import BollingerBands
from api.oanda_api import OandaApi
import time
import pandas as pd
from models.trade_decision import TradeDecision

# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)

# Constants
ADD_ROWS = 20
SLEEP = 10

# Is used to get the signal from a data frame


# Functions

def apply_signal(row, trade_settings: TradeSettings):
    """
    Get the signal from a data frame.

    Args:
        row (pd.DataFrame): The data frame row.
        trade_settings (TradeSettings): The trade settings.

    Returns:
        str: The signal.
    """
    #NOTE: A lot of logic for placing sell and buy signals are located in indicatory.py
    if row.SPREAD <= trade_settings.maxspread and row.GAIN >= trade_settings.mingain:
        if row.SELL_SIGNAL == -1:
            return defs.BUY
        elif row.BUY_SIGNAL == 1:
            return defs.SELL
    return defs.NONE


def apply_SL(row, trade_settings: TradeSettings):
    """
    Get the stop loss price from a data frame row.

    Args:
        row (pd.DataFrame): The data frame row.
        trade_settings (TradeSettings): The trade settings.

    Returns:
        float: The stop loss price.
    """
    if row.BUY_SIGNAL == 1:
        return row.mid_c + (abs(row.GAIN) * abs(trade_settings.LOSS_FACTOR))
    elif row.SELL_SIGNAL == -1:
        return row.mid_c - (abs(row.GAIN) * abs(trade_settings.PROFIT_FACTOR))
    return 0.0



def apply_TP(row, trade_settings: TradeSettings):
    """
    Get the take profit price from a data frame row.

    Args:
        row (pd.DataFrame): The data frame row.
+
    Returns:
        float: The take profit price.
    """

    if row.BUY_SIGNAL == 1:
       return row.mid_c + (abs(row.GAIN) * abs(trade_settings.PROFIT_FACTOR))
    elif row.SELL_SIGNAL == -1:
        return row.mid_c + (abs(row.GAIN) * abs(trade_settings.LOSS_FACTOR))
    return 0.0


def process_candles(df: pd.DataFrame, pair, trade_settings: TradeSettings, log_message):
    """
    Process the candles and get the trade decision.

    Args:
        df (pd.DataFrame): The candles data frame.
        pair (str): The pair.
        trade_settings (TradeSettings): The trade settings.
        log_message (func): The log message function.

    Returns:
        TradeDecision: The trade decision.
    """

    # Reset the index and add the `PAIR` column.

    df.reset_index(drop=True, inplace=True)
    df['PAIR'] = pair

    # Calculate the spread.

    df['SPREAD'] = df.ask_c - df.bid_c

    # Apply the Bollinger Bands indicator.

    df = BollingerBands(df, trade_settings.n_ma, trade_settings.n_std)

    # Calculate the gain and signal for each candle.

    df['GAIN'] = abs(df.mid_c - df.BB_MA)
    df['SIGNAL'] = df.apply(apply_signal, axis=1,
                            trade_settings=trade_settings)

    # Calculate the stop loss and take profit prices for each candle.

    df['TP'] = df.apply(apply_TP, axis=1, trade_settings=trade_settings)
    df['SL'] = df.apply(apply_SL, axis=1, trade_settings=trade_settings)
    df['LOSS'] = abs(df.mid_c - df.SL)

    # Get the last row of the data frame, which contains the trade decision.

    log_cols = ['PAIR', 'time', 'mid_c', 'mid_o',
                'SL', 'TP', 'SPREAD', 'GAIN', 'LOSS', 'SIGNAL']
    log_message(f"process_candles:\n{df[log_cols].tail()}", pair)

    return df[log_cols].iloc[-1]


def fetch_candles(pair, row_count, candle_time, granularity, api: OandaApi, log_message):

    retry_count = 0
    while retry_count < 3:
        time.sleep(SLEEP)
        df = api.get_candles_df(pair, count=row_count, granularity=granularity)

        if df.iloc[-1].time != candle_time:
            log_message(
                f"tech_manager fetch_candles {df.iloc[-1].time} not correct", pair)
            retry_count += 1

        if df is None or df.shape[0] == 0 and retry_count > 3:
            log_message(
                "tech_manger fetch_candles failed to get candles", pair)
            retry_count += 1

        if df is None or df.shape[0] == 0 or retry_count >= 3:
            log_message(
                "tech_manger fetch_candles failed to get candles", pair)
            return None
        print(df.empty)
        if df.empty == False:
            return df
        else:
            retry_count += 1


def get_trade_decision(candle_time, pair, granularity, api: OandaApi, trade_settings: TradeSettings, log_message):

    max_rows = trade_settings.n_ma + ADD_ROWS

    log_message(
        f"tech_manger: max_rows: {max_rows} candle_time: {candle_time} granularity: {granularity}", pair)

    df = fetch_candles(pair, max_rows, candle_time,
                       granularity, api, log_message)

    if df is not None:
        last_row = process_candles(df, pair, trade_settings, log_message)

        # A great way test how TP and SL works when trade is detected

        if last_row.SIGNAL != defs.NONE:
            log_message(f"SIGNAL:{last_row}\n", pair)

        return TradeDecision(last_row)

    return None
