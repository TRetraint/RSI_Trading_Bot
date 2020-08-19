import websocket
import json
import pandas as pd
import pickle
import talib
from datetime import datetime
from binance.client import Client
from binance.enums import *

#Binance Web Socket
SOCKET = 'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'
#Parameters of the RSI Strategy
RSI_PERIOD = 14
RSI_OVERBOUGHT =70
RSI_OVERSOLD = 30
#Symbol of Ethereum
TRADE_SYMBOL = "ETHUSD"
#Quantity of ETH for a trade
TRADE_QUANTITY = 1
in_position = False
df = pd.DataFrame()
API_KEY = 'xxx'
API_SECRET = 'xxx'

client = Client(API_KEY, API_SECRET)

#fonction to create an order
def order(symbol, qty, side, order_type=ORDER_TYPE_MARKET):
    try:
        order = client.create_order(symbol=symbol,
            side=side,
            type = order_type,
            quantity = qty)
        return True
    except Exception as e:
        return False

def on_open(ws):
    #Reading the data from a pickle file
    df.to_pickle("./close_prices.pkl")
    print("-----Open Connection-----")

def on_close(ws):
    #Saving the data into a pickle file
    df.to_pickle("./close_prices.pkl")
    print("-----Close Connection-----")


def on_message(ws, message):
    global candle
    global df
    global in_position
    json_message = json.loads(message)
    #getting only the candle details from the websocket's message
    candle = json_message['k']
    #candle['x'] inform about the end of the candle
    closed_candle = candle['x']
    close_price = candle['c']

    if closed_candle:
        #if the message is a closed candle, had it to the DataFrame
        df = df.append({'date' : datetime.fromtimestamp(candle['t']/1000),'close price': float(candle['c'])}, ignore_index=True)
        #Calling the RSI Strategy
        in_position = RSI_Strategy(close_price, df, in_position)



def RSI_Strategy(close_price, df, in_position):
    print("last close price : {}".format(close_price))
    #The RSI is computable with at least X Candles
    if len(df) > RSI_PERIOD:
        rsi = talib.RSI(df['close price'],RSI_PERIOD)
        #getting the lasr RSI
        last_rsi = rsi.iloc[-1]
        #Symbol is Overbought
        if last_rsi > RSI_OVERBOUGHT:
            #if in position
            if in_position:
                print("Sell")
                #Binance Sell Order
                order_success = order(TRADE_SYMBOL, TRADE_QUANTITY, SIDE_SELL, ORDER_TYPE_MARKET)
                #not anymore in position
                in_position = False
            else:
                print("No position hold")
        #Symbol is Oversold
        elif last_rsi < RSI_OVERSOLD:
            if in_position:
                print("Already in position")
            #If not in position
            else:
                print("Buy")
                #Binance Buy Order
                order_success = order(TRADE_SYMBOL, TRADE_QUANTITY, SIDE_BUY, ORDER_TYPE_MARKET)
                #In position
                in_position = True
    return in_position


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
