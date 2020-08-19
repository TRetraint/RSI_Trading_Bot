import yfinance as yf
import pandas as pd
import backtrader as bt
import backtrader.feeds as btfeeds
import datetime
from strategy import RSIStrategy

#getting data from Yahoo finance site
data = btfeeds.YahooFinanceCSVData(dataname='ETH_data.csv')
cerebro = bt.Cerebro()
#set cash to 10000$
starting_cash = 10000
cerebro.broker.set_cash(starting_cash)
#adding the data to backtrader
cerebro.adddata(data)
#adding the strategy
cerebro.addstrategy(RSIStrategy)
#Binance commision on trades
cerebro.broker.setcommission(0.001)

print('Starting Portfolio Value: {}'.format(cerebro.broker.getvalue()))

cerebro.run()

print('Final Portfolio Value: {}'.format(cerebro.broker.getvalue()))

print('Total winnings/losses : {}$'.format(cerebro.broker.getvalue() - starting_cash))
#plotting the results
cerebro.plot()