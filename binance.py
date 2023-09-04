import talib
import numpy as np
from binance.client import Client

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)

def calculate_rsi(symbol, interval, period):
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=100)
    closes = []
    for kline in klines:
        close_price = float(kline[4])
        closes.append(close_price)
    closes = np.array(closes)

    rsi = talib.RSI(closes, timeperiod=period)

    return rsi

symbol = 'BTCUSDT'
interval = '5m'
period = 14

rsi_data = calculate_rsi(symbol, interval, period)
print(rsi_data)
