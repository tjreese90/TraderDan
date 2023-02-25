class TradeDecision:
    
    def __init__(self, row):
        self.gain = row.GAIN
        self.signal = row.SIGNAL
        self.sl = row.SL
        self.tp = row.TP
        self.pair = row.PAIR
        
    def __repr__(self):
        return f"TradeDecision(): pair: {self.pair} dir:{self.signal} gain:{self.gain:.4f} s:{self.sl:.4f} tp:{self.tp:.4f}"