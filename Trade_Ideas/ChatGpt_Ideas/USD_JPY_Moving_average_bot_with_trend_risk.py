import oandapy
import pandas as pd

# Set up connection to Oanda API
oanda = oandapy.API(environment="practice", access_token="your_access_token")

# Set up parameters for moving averages
fast_ma_period = 10
slow_ma_period = 20

# Set up parameters for trade management
units = 1000
stop_loss_pips = 20
take_profit_pips = 50
trailing_stop_pips = 10

# Retrieve historical price data for USD/JPY
response = oanda.instrument.candles(instrument="USD_JPY", granularity="M1", count=slow_ma_period*2)
candles = response.get("candles")

# Convert price data to Pandas dataframe
df = pd.DataFrame(candles)
df["time"] = pd.to_datetime(df["time"])
df.set_index("time", inplace=True)
df["closeAsk"] = df["ask"].apply(lambda x: x["c"])

# Calculate moving averages
df["fast_ma"] = df["closeAsk"].rolling(fast_ma_period).mean()
df["slow_ma"] = df["closeAsk"].rolling(slow_ma_period).mean()

# Check if fast MA crosses above slow MA
if (df.iloc[-2]["fast_ma"] < df.iloc[-2]["slow_ma"]) and (df.iloc[-1]["fast_ma"] > df.iloc[-1]["slow_ma"]):
  # Place long trade
  response = oanda.order.market(
      account_id="your_account_id",
      instrument="USD_JPY",
      units=units,
      stop_loss=str(stop_loss_pips) + "pips",
      take_profit=str(take_profit_pips) + "pips"
  )

  # Set up trailing stop loss
  trade_id = response["id"]
  oanda.order.set_trailing_stop_loss(account_id="your_account_id", trade_id=trade_id, distance=str(trailing_stop_pips) + "pips")

# Check if fast MA crosses below slow MA
elif (df.iloc[-2]["fast_ma"] > df.iloc[-2]["slow_ma"]) and (df.iloc[-1]["fast_ma"] < df.iloc[-1]["slow_ma"]):
  # Place short trade
  response = oanda.order.market(
      account_id="your_account_id",
      instrument="USD_JPY",
      units=-units,
      stop_loss=str(stop_loss_pips) + "pips",
      take_profit=str(take_profit_pips) + "pips"
  )
