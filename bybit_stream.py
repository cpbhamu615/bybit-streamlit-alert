# bybit_stream.py

import websocket
import json
from threading import Thread
from data_buffer import buffer

prices = {}
candle_data = {
    "BTCUSDT": [],
    "ETHUSDT": [],
    "BNBUSDT": [],
    "SOLUSDT": []
}

def on_message(ws, message):
    msg = json.loads(message)
    if "topic" in msg and msg["topic"].startswith("kline"):
        symbol = msg["topic"].split(".")[-1]
        data = msg["data"][0]
        candle_data[symbol] = candle_data.get(symbol, [])
        candle_data[symbol].append(data)
        if len(candle_data[symbol]) > 100:
            candle_data[symbol] = candle_data[symbol][-100:]

    elif "topic" in msg and msg["topic"].startswith("tickers"):
        for ticker in msg["data"]:
            prices[ticker["symbol"]] = ticker["last_price"]

def on_open(ws):
    print("✅ WebSocket connected")
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
    for sym in symbols:
        ws.send(json.dumps({"op": "subscribe", "args": [f"kline.3.{sym}"]}))
    ws.send(json.dumps({"op": "subscribe", "args": ["tickers.BTCUSDT", "tickers.ETHUSDT", "tickers.BNBUSDT", "tickers.SOLUSDT"]}))

def start_websocket():
    def run():
        ws = websocket.WebSocketApp(
            "wss://stream.bybit.com/v5/public/linear",
            on_message=on_message,
            on_open=on_open
        )
        ws.run_forever()
    Thread(target=run).start()
