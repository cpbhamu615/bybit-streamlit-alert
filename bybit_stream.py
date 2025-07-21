# bybit_stream.py

import json
import threading
import websocket
from data_buffer import update_candles

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
interval = "3"  # 3-minute candles
candle_data = {}

def on_message(ws, message):
    msg = json.loads(message)
    if "topic" in msg and msg["topic"].startswith("kline"):
        data = msg["data"][0]
        topic = msg["topic"]
        symbol = topic.split(".")[-1]
        update_candles(symbol, data)

def on_open(ws):
    print("✅ Connected to Bybit WebSocket")
    for sym in symbols:
        sub_msg = {
            "op": "subscribe",
            "args": [f"kline.{interval}.{sym}"]
        }
        ws.send(json.dumps(sub_msg))

def start_websocket():
    url = "wss://stream.bybit.com/v5/public/linear"
    ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message)
    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()
