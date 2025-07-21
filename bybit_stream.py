# bybit_stream.py

import json
import threading
from websocket import WebSocketApp
from data_buffer import candle_data, prices

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

def on_message(ws, message):
    data = json.loads(message)
    if "topic" in data and "kline" in data["topic"]:
        symbol = data["topic"].split(".")[-1]
        kline = data["data"][0]
        candle_data[symbol].append(kline)
        if len(candle_data[symbol]) > 100:
            candle_data[symbol].pop(0)
    elif "topic" in data and "tickers" in data["topic"]:
        ticker = data["data"][0]
        symbol = ticker["symbol"]
        prices[symbol] = ticker["last_price"]

def on_open(ws):
    print("✅ Connected to Bybit WebSocket")
    sub = {
        "op": "subscribe",
        "args": [f"kline.3.{sym}" for sym in SYMBOLS] + [f"tickers.{sym}" for sym in SYMBOLS]
    }
    ws.send(json.dumps(sub))

def start_websocket():
    ws = WebSocketApp(
        "wss://stream.bybit.com/v5/public/linear",
        on_open=on_open,
        on_message=on_message,
    )
    threading.Thread(target=ws.run_forever, daemon=True).start()
