# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC
import pandas as pd
import numpy as np
# from keras.models import Sequential
# from keras.layers import LSTM, Dense

# Improved this code Tradingview.


def BollingerBands(df: pd.DataFrame, n=20, s=1.5, rsi_period=14, rsi_overbought=70, rsi_oversold=30):
    typical_p = (df.mid_c + df.mid_h + df.mid_l) / 3
    stddev = typical_p.ewm(span=n, min_periods=n - 1).std()
    df['BB_MA'] = typical_p.ewm(span=n, min_periods=n - 1).mean()
    df['BB_UP'] = df['BB_MA'] + stddev * s
    df['BB_LW'] = df['BB_MA'] - stddev * s
    
    # Band Width
    df['BB_WIDTH'] = df['BB_UP'] - df['BB_LW']
    
    # RSI (Relative Strength Index)
    delta = df['mid_c'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=rsi_period, min_periods=1).mean()
    avg_loss = loss.rolling(window=rsi_period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Basic Buy and Sell signals based on Bollinger Bands
    df['BUY_SIGNAL'] = np.where(df.mid_c < df['BB_LW'], 1, 0)
    df['SELL_SIGNAL'] = np.where(df.mid_c > df['BB_UP'], -1, 0)
    
    # Filtering signals using RSI
    df['BUY_SIGNAL'] = np.where((df['BUY_SIGNAL'] == 1) & (df['RSI'] < rsi_oversold), 1, 0)
    df['SELL_SIGNAL'] = np.where((df['SELL_SIGNAL'] == -1) & (df['RSI'] > rsi_overbought), -1, 0)
    
    # Slope of the Bollinger Bands
    df['BB_MA_SLOPE'] = df['BB_MA'].diff()
    df['BUY_SIGNAL'] = np.where((df['BUY_SIGNAL'] == 1) & (df['BB_MA_SLOPE'] > 0), 1, 0)
    df['SELL_SIGNAL'] = np.where((df['SELL_SIGNAL'] == -1) & (df['BB_MA_SLOPE'] < 0), -1, 0)
    
    # Combining signals into a single column
    df['SIGNAL'] = df['BUY_SIGNAL'] + df['SELL_SIGNAL']
    
    return df


# AVERAGE TRUE RANGE
def ATR(df: pd.DataFrame, n=14):
    prev_c = df.mid_c.shift(1)
    tr1 = df.mid_h - df.mid_l
    tr2 = abs(df.mid_h - prev_c)
    tr3 = abs(prev_c - df.mid_l)

    tr = pd.DataFrame({'tr1': tr1, 'tr2': tr2, 'tr3': tr3}).max(axis=1)
    df[f'ATR_{n}'] = tr.rolling(window=n).mean()
    return df


def KeltnerChannels(df: pd.DataFrame, n_ema=20, n_atr=10):
    df['EMA'] = df.mid_c.ewm(span=n_ema, min_periods=n_ema).mean()
    df = ATR(df, n=n_atr)
    c_atr = f"ATR_{n_atr}"
    df['KeUP'] = df[c_atr] * 2 + df.EMA
    df['KeLO'] = df.EMA - df[c_atr] * 2
    df.drop(c_atr, axis=1, inplace=True)
    return df


def RSI(df: pd.DataFrame, n=14):
    alpha = 1.0 / n
    gains = df.mid_c.diff()

    wins = pd.Series([x if x >= 0 else 0.0 for x in gains], name="wins")
    losses = pd.Series(
        [x * -1 if x < 0 else 0.0 for x in gains], name="losses")

    wins_rma = wins.ewm(min_periods=n, alpha=alpha).mean()
    losses_rma = losses.ewm(min_periods=n, alpha=alpha).mean()

    rs = wins_rma / losses_rma

    df[f"RSI_{n}"] = 100.0 - (100.0 / (1.0 + rs))
    return df


def MACD(df: pd.DataFrame, n_slow=26, n_fast=12, n_signal=9):

    ema_long = df.mid_c.ewm(min_periods=n_slow, span=n_slow).mean()
    ema_short = df.mid_c.ewm(min_periods=n_fast, span=n_fast).mean()

    df['MACD'] = ema_short - ema_long
    df['SIGNAL'] = df.MACD.ewm(min_periods=n_signal, span=n_signal).mean()
    df['HIST'] = df.MACD - df.SIGNAL

    return df


# ChatGPT 1 Stragey Regular RSI, MACD, BollingerBands
def EnhancedTradingIndicator(df: pd.DataFrame, n_bb=20, s_bb=1.5, n_rsi=14, n_slow=26, n_fast=12, n_signal=9):
    typical_p = (df.mid_c + df.mid_h + df.mid_l) / 3
    stddev = typical_p.ewm(span=n_bb, min_periods=n_bb - 1).std()
    df['BB_MA'] = typical_p.ewm(span=n_bb, min_periods=n_bb - 1).mean()
    df['BB_UP'] = df['BB_MA'] + stddev * s_bb
    df['BB_LW'] = df['BB_MA'] - stddev * s_bb

    df['RSI'] = RSI(df, n=n_rsi)[f"RSI_{n_rsi}"]
    df = MACD(df, n_slow=n_slow, n_fast=n_fast, n_signal=n_signal)

    df['BUY_SIGNAL'] = np.where(
        (df.mid_c > df['BB_UP']) & (df.RSI < 30) & (df.HIST > 0), 1, 0)

    df['SELL_SIGNAL'] = np.where(
        (df.mid_c < df['BB_LW']) | (df.RSI > 70) | (df.HIST < 0), -1, 0)

    df['SIGNAL'] = df['BUY_SIGNAL'] | df['SELL_SIGNAL']
    df['SIGNAL'].replace(to_replace=0, method='ffill', inplace=True)

    return df

# ChatGPT 2 Stragey MACD, RSI, and ATR


def CustomTradingIndicator(df: pd.DataFrame, n_slow=26, n_fast=12, n_signal=9, n_rsi=14, n_atr=14):
    df = MACD(df, n_slow=n_slow, n_fast=n_fast, n_signal=n_signal)
    df = RSI(df, n=n_rsi)
    df = ATR(df, n=n_atr)

    df['BUY_SIGNAL'] = np.where(
        (df.MACD > df.SIGNAL) & (df.RSI < 30) & (df.mid_c > df.mid_c.shift(1)) & (df.mid_c.shift(1) > df.mid_c.shift(2)) & (df.mid_c > df.mid_c.rolling(5).mean()) & (df.mid_c > df.mid_c.rolling(20).mean()), 1, 0)

    df['SELL_SIGNAL'] = np.where(
        (df.MACD < df.SIGNAL) & (df.RSI > 70) & (df.mid_c < df.mid_c.shift(1)) & (df.mid_c.shift(1) < df.mid_c.shift(2)) & (df.mid_c < df.mid_c.rolling(5).mean()) & (df.mid_c < df.mid_c.rolling(20).mean()), -1, 0)

    df['SIGNAL'] = df['BUY_SIGNAL'] | df['SELL_SIGNAL']
    df['SIGNAL'].replace(to_replace=0, method='ffill', inplace=True)

    return df


# ChatGPT ML Indicator


def MLTradingIndicator(df: pd.DataFrame, n_slow=26, n_fast=12, n_signal=9, n_rsi=14):
    df = MACD(df, n_slow=n_slow, n_fast=n_fast, n_signal=n_signal)
    df = RSI(df, n=n_rsi)

    # Prepare the features and target variables
    X = df[['MACD', f"RSI_{n_rsi}"]].values
    # Target variable: 1 for buy, -1 for sell
    y = np.where(df.mid_c.shift(-1) > df.mid_c, 1, -1)

    # Train the Support Vector Machine classifier
    svm = SVC(kernel='linear')
    svm.fit(X, y)

    # Predict the labels for the current data
    predictions = svm.predict(X)

    df['SIGNAL'] = predictions
    df['SIGNAL'].replace(to_replace=-1, method='ffill', inplace=True)

    return df


# ChatGPT ML stratergy number 2


def BestTradingIndicator(df: pd.DataFrame, n_slow=26, n_fast=12, n_signal=9, n_rsi=14, n_atr=14):
    df = MACD(df, n_slow=n_slow, n_fast=n_fast, n_signal=n_signal)
    df = RSI(df, n=n_rsi)
    df = ATR(df, n=n_atr)

    # Prepare the features and target variables
    X = df[['MACD', f"RSI_{n_rsi}", f"ATR_{n_atr}"]].values
    # Target variable: 1 for buy, -1 for sell
    y = np.where(df.mid_c.shift(-1) > df.mid_c, 1, -1)

    # Train a Random Forest classifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)

    # Predict the labels for the current data
    predictions = rf.predict(X)

    df['SIGNAL'] = predictions
    df['SIGNAL'].replace(to_replace=-1, method='ffill', inplace=True)

    return df

# Volume Weighted Average Price (VWAP):


def VWAP(df: pd.DataFrame, ma_window=20):
    cumulative_volume = df['volume'].cumsum()
    cumulative_pv = (df['mid_c'] * df['volume']).cumsum()
    vwap = cumulative_pv / cumulative_volume

    # Calculate the moving average of VWAP
    vwap_ma = vwap.rolling(window=ma_window).mean()

    # Generate signals
    df['BUY_SIGNAL'] = np.where(
        (df['mid_c'] > vwap) & (df['mid_c'] > vwap_ma), 1, 0)
    df['SELL_SIGNAL'] = np.where(
        (df['mid_c'] < vwap) & (df['mid_c'] < vwap_ma), -1, 0)

    return df


# Ichimoku Cloud:
def IchimokuCloud(df: pd.DataFrame):
    conversion_line = (df['mid_h'].rolling(window=9).max() +
                       df['mid_l'].rolling(window=9).min()) / 2
    base_line = (df['mid_h'].rolling(window=26).max() +
                 df['mid_l'].rolling(window=26).min()) / 2
    leading_span_a = (conversion_line + base_line) / 2
    leading_span_b = (df['mid_h'].rolling(window=52).max() +
                      df['mid_l'].rolling(window=52).min()) / 2
    lagging_span = df['mid_c'].shift(-26)

    df['BUY_SIGNAL'] = np.where((df['mid_c'] > leading_span_a) & (
        df['mid_c'] > leading_span_b) & (df['mid_c'] > lagging_span), 1, 0)
    df['SELL_SIGNAL'] = np.where((df['mid_c'] < leading_span_a) & (
        df['mid_c'] < leading_span_b) & (df['mid_c'] < lagging_span), -1, 0)

    return df

# FibonacciRetracement Stragery


def FibonacciRetracement(df: pd.DataFrame, start_price, end_price, confirmation_pct=0.5):
    # Calculate Fibonacci retracement levels
    levels = [0, 0.382, 0.5, 0.618, 1.0]

    price_range = end_price - start_price
    retracement_levels = [start_price +
                          level * price_range for level in levels]

    # Calculate the confirmation threshold
    confirmation_level = start_price + confirmation_pct * price_range

    df['BUY_SIGNAL'] = np.where((df['mid_c'] <= retracement_levels[1]) & (
        df['mid_c'] >= confirmation_level), 1, 0)
    df['SELL_SIGNAL'] = np.where((df['mid_c'] >= retracement_levels[3]) & (
        df['mid_c'] <= confirmation_level), -1, 0)

    return df


# Complex multi-level indicator.


def BestTradingIndicator(df: pd.DataFrame, n_slow=26, n_fast=12, n_signal=9, n_rsi=14, n_atr=14):
    df = MACD(df, n_slow=n_slow, n_fast=n_fast, n_signal=n_signal)
    df = RSI(df, n=n_rsi)
    df = ATR(df, n=n_atr)

    # Prepare the features and target variables
    X = df[['MACD', f"RSI_{n_rsi}", f"ATR_{n_atr}"]].values
    # Target variable: 1 for buy, -1 for sell
    y = np.where(df.mid_c.shift(-1) > df.mid_c, 1, -1)

    # Train a Random Forest classifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)

    # Predict the labels for the current data
    predictions = rf.predict(X)

    df['SIGNAL'] = predictions
    df['SIGNAL'].replace(to_replace=-1, method='ffill', inplace=True)

    return df


def BollingerBands(df: pd.DataFrame, n=20, s=1.5):
    typical_p = (df.mid_c + df.mid_h + df.mid_l) / 3
    stddev = typical_p.ewm(span=n, min_periods=n - 1).std()
    df['BB_MA'] = typical_p.ewm(span=n, min_periods=n - 1).mean()
    df['BB_UP'] = df['BB_MA'] + stddev * s
    df['BB_LW'] = df['BB_MA'] - stddev * s

    df['BUY_SIGNAL'] = np.where(df.mid_c > df['BB_UP'], 1, 0)
    df['SELL_SIGNAL'] = np.where(
        (df.mid_c < df['BB_LW']) | (df.mid_c > df['BB_UP']), -1, 0)

    df['SIGNAL'] = df['BUY_SIGNAL'] | df['SELL_SIGNAL']
    df['SIGNAL'].replace(to_replace=0, method='ffill', inplace=True)

    return df

# Other indicator functions...

# Combine the indicators to create the best indicator


def SmartIndicator(df: pd.DataFrame):
    df = BestTradingIndicator(df)
    df = BollingerBands(df)

    # Generate final signals based on the combined indicators
    df['BUY_SIGNAL'] = np.where(
        (df['SIGNAL'] == 1) & (df['BB_MA'] > df['BB_UP']), 1, 0)
    df['SELL_SIGNAL'] = np.where(
        (df['SIGNAL'] == -1) & (df['BB_MA'] < df['BB_LW']), -1, 0)

    return df


# One more ML stragery

# Define indicator functions...


def SmartIndicator(df: pd.DataFrame):
    df = MACD(df)
    df = RSI(df)
    df = ATR(df)
    df = BollingerBands(df)

    # Prepare the features and target variables
    X = df[['MACD', f"RSI_{n_rsi}", f"ATR_{n_atr}",
            'BB_MA', 'BB_UP', 'BB_LW']].values
    # Target variable: 1 for buy, -1 for sell
    y = np.where(df.mid_c.shift(-1) > df.mid_c, 1, -1)

    # Train the Support Vector Machine classifier
    svm = SVC(kernel='linear')
    svm.fit(X, y)

    # Predict the labels for the current data
    predictions = svm.predict(X)

    df['SIGNAL'] = predictions
    df['SIGNAL'].replace(to_replace=-1, method='ffill', inplace=True)

    return df

# Indicatorss and Patterns together strageies.


def BollingerBandsWithEngulfing(df: pd.DataFrame, n=20, s=1.5):
    typical_p = (df.mid_c + df.mid_h + df.mid_l) / 3
    stddev = typical_p.ewm(span=n, min_periods=n - 1).std()
    df['BB_MA'] = typical_p.ewm(span=n, min_periods=n - 1).mean()
    df['BB_UP'] = df['BB_MA'] + stddev * s
    df['BB_LW'] = df['BB_MA'] - stddev * s

    df['BUY_SIGNAL'] = np.where(df.mid_c > df['BB_UP'], 1, 0)
    df['SELL_SIGNAL'] = np.where(
        (df.mid_c < df['BB_LW']) | (df.mid_c > df['BB_UP']), -1, 0)

    # Apply Bullish Engulfing and Bearish Engulfing pattern logic
    df['BULLISH_ENGULFING'] = df.apply(apply_engulfing, axis=1)
    df['BEARISH_ENGULFING'] = df.apply(apply_engulfing, axis=1)

    # Generate combined signals
    df['SIGNAL'] = np.where((df['BUY_SIGNAL'] & df['BULLISH_ENGULFING']) | (
        df['SELL_SIGNAL'] & df['BEARISH_ENGULFING']), 1, -1)
    df['SIGNAL'].replace(to_replace=0, method='ffill', inplace=True)

    return df

# USDJPY PRICE ACTION STRAT
def USDJPY_PriceActionSuite(df: pd.DataFrame):
    # Calculate price range
    price_range = df['mid_h'] - df['mid_l']

    # Calculate LTA levels
    lta_threshold = 0.3  # Adjust the LTA threshold as desired
    lta_level = df['mid_l'] + lta_threshold * price_range
    hta_level = df['mid_h'] - lta_threshold * price_range

    # Calculate confirmation levels
    confirmation_pct = 0.5  # Adjust the confirmation percentage as desired
    confirmation_level = df['mid_l'] + confirmation_pct * price_range

    # Calculate Engulfing pattern thresholds
    engulfing_factor = 1.5  # Adjust the engulfing factor as desired
    engulfing_confirmation = df['mid_l'] + engulfing_factor * price_range

    # Calculate Pin Bar thresholds
    pin_bar_threshold = 0.5  # Adjust the pin bar threshold as desired

    # Initialize signals
    df['BUY_SIGNAL'] = 0
    df['SELL_SIGNAL'] = 0

    # Generate signals based on LTAs
    for i in range(1, len(df)):
        if df['mid_c'][i] > lta_level[i] and df['mid_c'][i] > confirmation_level[i-1]:
            # Bullish signal if above LTA level and confirmation level
            df['BUY_SIGNAL'][i] = 1
        elif df['mid_c'][i] < hta_level[i] and df['mid_c'][i] < confirmation_level[i-1]:
            # Bearish signal if below LTA level and confirmation level
            df['SELL_SIGNAL'][i] = -1

    # Apply Engulfing pattern signals
    df['ENGULFING_BUY_SIGNAL'] = np.where(
        (df['mid_c'] > df['mid_o'].shift(1)) &
        (df['mid_o'] < df['mid_c'].shift(1)) &
        (df['mid_c'] > engulfing_confirmation.shift(1)), 1, 0
    )

    df['ENGULFING_SELL_SIGNAL'] = np.where(
        (df['mid_c'] < df['mid_o'].shift(1)) &
        (df['mid_o'] > df['mid_c'].shift(1)) &
        (df['mid_c'] < engulfing_confirmation.shift(1)), -1, 0
    )

    # Apply Pin Bar signals
    df['PIN_BAR_BUY_SIGNAL'] = np.where(
        (df['mid_c'] > df['mid_h'].shift(1)) &
        ((df['mid_o'] - df['mid_l']) > pin_bar_threshold *
         (df['mid_h'] - df['mid_l'])), 1, 0
    )

    df['PIN_BAR_SELL_SIGNAL'] = np.where(
        (df['mid_c'] < df['mid_l'].shift(1)) &
        ((df['mid_h'] - df['mid_o']) > pin_bar_threshold *
         (df['mid_h'] - df['mid_l'])), -1, 0
    )

    # Combine signals
    df['SIGNAL'] = (
        df['BUY_SIGNAL'] + df['SELL_SIGNAL'] +
        df['ENGULFING_BUY_SIGNAL'] + df['ENGULFING_SELL_SIGNAL'] +
        df['PIN_BAR_BUY_SIGNAL'] + df['PIN_BAR_SELL_SIGNAL']
    )

    return df

# Price Action Suite


def PriceActionSuite(df: pd.DataFrame, lta_threshold=0.5, engulfing_factor=1.5, pin_bar_threshold=0.5):
    # Calculate price range
    price_range = df['mid_h'] - df['mid_l']

    # Calculate LTA levels
    lta_level = df['mid_l'] + lta_threshold * price_range
    hta_level = df['mid_h'] - lta_threshold * price_range

    # Calculate confirmation levels for engulfing patterns
    engulfing_confirmation = df['mid_l'] + engulfing_factor * price_range

    # Initialize signals
    df['BUY_SIGNAL'] = 0
    df['SELL_SIGNAL'] = 0

    # Generate signals based on LTAs
    for i in range(1, len(df)):
        if df['mid_c'][i] > lta_level[i]:
            # Bullish signal if above LTA level
            df['BUY_SIGNAL'][i] = 1
        elif df['mid_c'][i] < hta_level[i]:
            # Bearish signal if below LTA level
            df['SELL_SIGNAL'][i] = -1

    # Apply Engulfing pattern signals
    df['ENGULFING_BUY_SIGNAL'] = np.where(
        (df['mid_c'] > df['mid_o'].shift(1)) &
        (df['mid_o'] < df['mid_c'].shift(1)) &
        (df['mid_c'] > engulfing_confirmation.shift(1)), 1, 0
    )

    df['ENGULFING_SELL_SIGNAL'] = np.where(
        (df['mid_c'] < df['mid_o'].shift(1)) &
        (df['mid_o'] > df['mid_c'].shift(1)) &
        (df['mid_c'] < engulfing_confirmation.shift(1)), -1, 0
    )

    # Apply Pin Bar signals
    df['PIN_BAR_BUY_SIGNAL'] = np.where(
        (df['mid_c'] > df['mid_h'].shift(1)) &
        ((df['mid_o'] - df['mid_l']) > pin_bar_threshold *
         (df['mid_h'] - df['mid_l'])), 1, 0
    )

    df['PIN_BAR_SELL_SIGNAL'] = np.where(
        (df['mid_c'] < df['mid_l'].shift(1)) &
        ((df['mid_h'] - df['mid_o']) > pin_bar_threshold *
         (df['mid_h'] - df['mid_l'])), -1, 0
    )

    # Combine signals
    df['SIGNAL'] = (
        df['BUY_SIGNAL'] + df['SELL_SIGNAL'] +
        df['ENGULFING_BUY_SIGNAL'] + df['ENGULFING_SELL_SIGNAL'] +
        df['PIN_BAR_BUY_SIGNAL'] + df['PIN_BAR_SELL_SIGNAL']
    )

    return df

# PinBar Reversal


def PinBarReversal(df: pd.DataFrame, pin_bar_threshold=0.5):
    df['Pin_Bar'] = np.where(
        (df['mid_h'] - df['mid_l']) > pin_bar_threshold * (df['mid_o'] - df['mid_c']) &
        (df['mid_o'] > df['mid_c']) &
        (df['mid_c'] < df['mid_l'] + 0.5 * (df['mid_h'] - df['mid_l'])) &
        (df['mid_o'] < df['mid_l'] + 0.5 * (df['mid_h'] - df['mid_l'])), 1, 0
    )

    df['BUY_SIGNAL'] = np.where(
        (df['Pin_Bar'] == 1) &
        (df['mid_c'] > df['mid_h'].shift(1)), 1, 0
    )

    df['SELL_SIGNAL'] = np.where(
        (df['Pin_Bar'] == 1) &
        (df['mid_c'] < df['mid_l'].shift(1)), -1, 0
    )

    return df

# InsideBarBreak Out stratgy


def InsideBarBreakout(df: pd.DataFrame):
    df['Inside_Bar'] = np.where(
        (df['mid_h'].shift(1) > df['mid_h']) &
        (df['mid_l'].shift(1) < df['mid_l']) &
        (df['mid_h'].shift(1) - df['mid_l'].shift(1)
         > df['mid_h'] - df['mid_l']), 1, 0
    )

    df['BUY_SIGNAL'] = np.where(
        (df['mid_h'] > df['mid_h'].shift(1)) &
        (df['mid_l'] < df['mid_l'].shift(1)) &
        (df['Inside_Bar'] == 1), 1, 0
    )

    df['SELL_SIGNAL'] = np.where(
        (df['mid_h'] < df['mid_h'].shift(1)) &
        (df['mid_l'] > df['mid_l'].shift(1)) &
        (df['Inside_Bar'] == 1), -1, 0
    )

    return df

# Low Traffic Areas Price Action Strat


def LTA_PriceActionStrategy(df: pd.DataFrame, threshold=0.5, confirmation_pct=0.5):
    # Calculate price range
    price_range = df['mid_h'] - df['mid_l']

    # Calculate LTA levels
    lta_level = df['mid_l'] + threshold * price_range
    hta_level = df['mid_h'] - threshold * price_range

    # Calculate confirmation threshold
    confirmation_level = df['mid_l'] + confirmation_pct * price_range

    # Initialize signals
    df['BUY_SIGNAL'] = 0
    df['SELL_SIGNAL'] = 0

    # Generate signals based on LTAs
    for i in range(1, len(df)):
        if df['mid_c'][i] > lta_level[i] and df['mid_c'][i] > confirmation_level[i-1]:
            df['BUY_SIGNAL'][i] = 1
        elif df['mid_c'][i] < hta_level[i] and df['mid_c'][i] < confirmation_level[i-1]:
            df['SELL_SIGNAL'][i] = -1

    return df

# Another custom ML Smart Indicator.
def SmartMLIndicator(df: pd.DataFrame):
    df = MACD(df)
    df = RSI(df)
    df = ATR(df)
    df = BollingerBands(df)

    # Prepare the features and target variables
    X = df[['MACD', f"RSI_{n_rsi}", f"ATR_{n_atr}", 'BB_MA', 'BB_UP', 'BB_LW']].values
    # Target variable: 1 for buy, -1 for sell
    y = np.where(df.mid_c.shift(-1) > df.mid_c, 1, -1)

    # Build a neural network model
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=X.shape[1]))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(X, y, epochs=10, batch_size=32)

    # Predict the labels for the current data
    predictions = model.predict(X)
    predictions = np.where(predictions > 0.5, 1, -1)

    df['BUY_SIGNAL'] = np.where(predictions == 1, 1, 0)
    df['SELL_SIGNAL'] = np.where(predictions == -1, -1, 0)

    return df

# # Moving Average CrossOver with LSTM ML ALGO

# def LTA_PriceActionStrategy(df: pd.DataFrame):
    
#     data = pd.read_csv('forex_data.csv')
    
#     #create train /test sets 
#     train = data[:int(0.7 * len(data))]
#     test = data[int(0.7 * len(data)):]
    
#     #Create input/output sequences
    
#     seq_len = 50
#     in_seq1 = data['50ma'].values
#     in_seq2 = data['200na'].values
#     out_seq = np.zeros(len(data))
#     out_seq[np.where(in_seq1 > in_seq2)[0]] = 1
    
#     # Reshape into input/output
    
#     x_train = train[in_seq1].values.reshape(len(train), seq_len, 1)
#     y_train = train[out_seq].values
#     y_test =test[out_seq].values
    
#     # Creating the LSTM Learning model.
    
#     model = Sequential()
#     model.add(LSTM(50,input_shape=(seq_len, 1)))
#     model.add(Dense(1, activation='sigmoid'))
#     model.compile(optimize='adam', loss='binary_crossentropy', metrics=['accuracy'])

#     # Creating FIT Model
    
#     model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=1) 
    
#     # Generate signals on test data    