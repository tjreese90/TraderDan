from bot.bot import Bot
from instrumentCollection.instrument_collection import instrumentCollection as ic

if __name__ == "__main__":
    ic.LoadInstrumentsDB()
    b = Bot()
    b.run()