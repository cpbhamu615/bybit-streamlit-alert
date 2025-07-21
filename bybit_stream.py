# bybit_stream.py

import websocket, json
from threading import Thread
from data_buffer import candle_data, prices

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

def on_message(ws, message):
    print("MESSAGE RECEIVED:", message)  
    data = json.loads(message)
    if 'topic' not in data: return
    topic = data['topic']

    if topic.startswith("kline.3."):
        symbol = topic.split('.')[-1]
        k = data["data"]
        candle = {
            "timestamp": k["start"],
            "open": float(k["open"]),
            "high": float(k["high"]),
            "low": float(k["low"]),
            "close": float(k["close"])
        }
        if symbol in candle_data:
            candle_data[symbol].append(candle)
            if len(candle_data[symbol]) > 100:
                candle_data[symbol].pop(0)

    elif topic.startswith("tickers."):
        for t in data["data"]:
            symbol = t["symbol"]
            if symbol in prices:
                prices[symbol] = float(t["lastPrice"])

def on_open(ws):
    args = [f"kline.3.{s}" for s in SYMBOLS]
    args += [f"tickers.{s}" for s in SYMBOLS]
    ws.send(json.dumps({"op": "subscribe", "args": args}))

def start_websocket():
    def run():
        ws = websocket.WebSocketApp(
            "wss://stream.bybit.com/v5/public/spot"
            on_open=on_open,
            on_message=on_message
        )
        ws.run_forever()
    Thread(target=run, daemon=True).start()
