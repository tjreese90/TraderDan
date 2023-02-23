import datetime as dt

class CandleTiming:
    
    def __init__(self, last_time):
        self.last_time = last_time
        self.is_ready = False
        
    def __repr__(self) -> str:
        return f"last_candle:{dt.datetime.strftime(self.last_time, '%y-%m-%d %H:%M')} is ready:{self.is_ready}"
        