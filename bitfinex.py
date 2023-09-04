import websocket
import json

bitfinex_ws_url = 'wss://api-pub.bitfinex.com/ws/2'

vwap_data = {'sum_price_volume': 0, 'sum_volume': 0}


def on_message(ws, message):
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

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print('Closed')

def on_open(ws):
    print('Open')
    subscribe_data = {
        'event': 'subscribe',
        'channel': 'candles',
        'key': 'trade:1m:tBTCUSD'
    }
    ws.send(json.dumps(subscribe_data))

bitfinex_ws = websocket.WebSocketApp(
    bitfinex_ws_url,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)
bitfinex_ws.on_open = on_open
bitfinex_ws.run_forever()
