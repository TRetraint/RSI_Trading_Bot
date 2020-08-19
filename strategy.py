import backtrader as bt

#class to create a Strategy
class RSIStrategy(bt.Strategy):
    #log function
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s: %s' % (dt.isoformat(), txt))

    #initialisation function
    def __init__(self):
        #declare a rsi variable
        self.rsi = bt.indicators.RSI(self.data, period = 14)
        #in position variable
        self.in_position = False

    def next(self):
        #if the symbol is overbought
        if self.rsi[0] > 70:
            #if in position is true, sell
            if self.in_position:
                print("Sell")
                self.sell()
                self.in_position = False
            else:
                pass
        #if the symbol is oversold
        elif self.rsi[0] < 30:
            if self.in_position:
                pass
            #buy if not in position
            else:
                print("Buy")
                self.buy()
                self.in_position = True
