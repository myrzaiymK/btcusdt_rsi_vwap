import websocket
import json
import numpy as np
from binance.client import Client
import talib

api_key_binance = ''
api_secret_binance = ''
bitfinex_ws_url = 'wss://api-pub.bitfinex.com/ws/2'

vwap_data = {'sum_price_volume': 0, 'sum_volume': 0}

client_binance = Client(api_key_binance, api_secret_binance)

def calculate_rsi(symbol, interval, period):
    klines = client_binance.futures_klines(symbol=symbol, interval=interval, limit=100)
    closes = []
    for kline in klines:
        close_price = float(kline[4])
        closes.append(close_price)
    closes = np.array(closes)
    rsi = talib.RSI(closes, timeperiod=period)
    return rsi


def on_message_bitfinex(ws, message):
    global vwap_data
    msg = json.loads(message)
    if isinstance(msg, list) and len(msg) > 1:
        candle_data = msg[1]
        if isinstance(candle_data, list) and len(candle_data) > 2:
            close_price = candle_data[2]
            volume = candle_data[5]
            vwap_data['sum_price_volume'] += close_price * volume
            vwap_data['sum_volume'] += volume
            vwap = vwap_data['sum_price_volume'] / vwap_data['sum_volume']
            if vwap is not None:
                print(f'Bitfinex Close Price: {close_price}, VWAP: {vwap:.2f}')


def on_message_binance(ws, message):
    global vwap_data
    msg = json.loads(message)
    if 'k' in msg:
        candle_data = msg['k']
        close_price = float(candle_data['c'])
        volume = float(candle_data['v'])
        vwap_data['sum_price_volume'] += close_price * volume
        vwap_data['sum_volume'] += volume
        vwap = vwap_data['sum_price_volume'] / vwap_data['sum_volume']
        if vwap is not None:
            print(f'Binance Close Price: {close_price}, VWAP: {vwap:.2f}')


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print('Closed')


def on_open(ws):
    print('Opened')

    subscribe_data_bitfinex = {
        'event': 'subscribe',
        'channel': 'candles',
        'key': 'trade:1m:tBTCUSD'
    }
    ws.send(json.dumps(subscribe_data_bitfinex))


symbol = 'BTCUSDT'
interval = '5m'
period = 14

if __name__=='__main__':
    rsi_data = calculate_rsi(symbol, interval, period)
    print(rsi_data)

    bitfinex_ws = websocket.WebSocketApp(
        bitfinex_ws_url,
        on_message=on_message_bitfinex,
        on_error=on_error,
        on_close=on_close
    )
    bitfinex_ws.on_open = on_open
    bitfinex_ws.run_forever()
