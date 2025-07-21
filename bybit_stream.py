# bybit_stream.py

import websocket
import json
from threading import Thread
from data_buffer import candle_data, prices

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

def on_message(ws, message):
    data = json.loads(message)
    if 'topic' not in data: return

    topic = data['topic']
    
    if topic.startswith("kline.3m."):
        symbol = topic.split(".")[-1]
        kline = data["data"]
        candle = {
            "timestamp": kline["start"],
            "open": float(kline["open"]),
            "high": float(kline["high"]),
            "low": float(kline["low"]),
            "close": float(kline["close"])
        }
        if symbol in candle_data:
            candles = candle_data[symbol]
            candles.append(candle)
            if len(candles) > 100:
                candles.pop(0)
    
    elif topic.startswith("tickers."):
        for ticker in data["data"]:
            symbol = ticker["symbol"]
            if symbol in prices:
                prices[symbol] = float(ticker["lastPrice"])

def on_open(ws):
    sub_msgs = []

    for symbol in SYMBOLS:
        sub_msgs.append({
            "op": "subscribe",
            "args": [f"kline.3m.{symbol}"]
        })
    sub_msgs.append({
        "op": "subscribe",
        "args": ["tickers"]
    })

    for msg in sub_msgs:
        ws.send(json.dumps(msg))

def start_websocket():
    def run():
        ws = websocket.WebSocketApp(
            "wss://stream.bybit.com/v5/public/linear",
            on_open=on_open,
            on_message=on_message
        )
        ws.run_forever()

    Thread(target=run, daemon=True).start()
