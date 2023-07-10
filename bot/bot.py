import json
import time
from bot.trade_manger import place_trade
import constants.defs as defs
from bot.technicals_manger import get_trade_decision
from instrumentCollection.log_wrapper import LogWrapper
from models.trade_settings import TradeSettings
from api.oanda_api import OandaApi
from bot.candle_manager import CandleManger

# Summary:
# The bot file contains a class called Bot that initializes
#  the bot by loading settings from a JSON file, setting up logs,
#  initializing an Oanda API object and a CandleManager object.
#  It also has methods for processing candle data, logging messages
#  to appropriate logs, and placing trades. The run method of the Bot
#  class updates the timings of the candles and processes them in a loop with a
#  specified sleep time. If triggered pairs are found, it makes trade decisions based on candle
#  data and places trades.


class Bot:

    # Constants for error and main logs, candle granularity, and sleep time between processing candles
    ERROR_LOG = "error"
    MAIN_LOG = "main"
    GRANULARITY = "M5"
    SLEEP = 120

    def __init__(self):
        # Load settings from settings.json file and set up logs
        self.load_settings()
        self.setup_logs()

        # Initialize Oanda API and CandleManager objects
        self.api = OandaApi()
        self.candle_manger = CandleManger(
            self.api, self.trade_settings, self.log_message, Bot.GRANULARITY)

        # Log bot start and failure messages
        self.log_to_main("Bot Started")
        self.log_to_error("Bot Failed")

    def load_settings(self):
        # Load settings from settings.json file and create TradeSettings objects for each pair
        with open("./bot/settings.json", "r") as f:
            data = json.loads(f.read())
            self.trade_settings = {k: TradeSettings(
                v, k) for k, v in data['pairs'].items()}
            self.trade_risk = data['trade_risk']

    def setup_logs(self):
        # Set up logs for each pair and error/main logs
        self.logs = {}
        for k in self.trade_settings.keys():
            self.logs[k] = LogWrapper(k)
            self.log_message(f"{self.trade_settings[k]}", k)
        self.logs[Bot.ERROR_LOG] = LogWrapper(Bot.ERROR_LOG)
        self.logs[Bot.MAIN_LOG] = LogWrapper(Bot.MAIN_LOG)
        self.log_to_main(
            f"Bot started with {TradeSettings.settings_to_str(self.trade_settings)}")

    def log_message(self, msg, key):
        # Log a message to the appropriate log based on the key
        self.logs[key].logger.debug(msg)

    def log_to_main(self, msg):
        # Log a message to the main log
        self.log_message(msg, Bot.MAIN_LOG)

    def log_to_error(self, msg):
        # Log a message to the error log
        self.log_message(msg, Bot.ERROR_LOG)

    def process_candles(self, triggered):
        # Process triggered pairs and make trade decisions based on candle data
        if len(triggered) > 0:
            self.log_message(
                f"process_candles triggerd:{triggered}", Bot.MAIN_LOG)
            for p in triggered:
                last_time = self.candle_manger.timings[p].last_time
                trade_decision = get_trade_decision(
                    last_time, p, Bot.GRANULARITY, self.api, self.trade_settings[p], self.log_message)

                if trade_decision is not None and trade_decision.signal != defs.NONE:
                    self.log_message(f"Place Trade: {trade_decision}", p)
                    self.log_to_main(f"Place Trade: {trade_decision}")
                    # Place Trade Logic will go here
                    place_trade(trade_decision, self.api, self.log_message,
                                self.log_to_error, self.trade_risk)
        else:
            self.log_to_error(
                f"Failed to Start Process Candles since {triggered} is not defined")

            # You can add a Try Catch here if you find errors process_candles"
    def run(self):
        # Wait for a specified amount of time before executing the next iteration of the loop
        while True:
            time.sleep(Bot.SLEEP)
            # Update the timings of the candles and process them
            self.process_candles(self.candle_manger.update_timings())
            # Print the result of the process_candles function
            print(
                f"Result of using process_candles {self.candle_manger.update_timings()} do I get a trigger back?")
