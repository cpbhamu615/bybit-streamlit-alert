# bybit_stream.py
import websocket
import json
import threading
import time
from collections import defaultdict

symbol_list = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
interval = "3"  # 3-minute candles

candle_data = defaultdict(list)  # symbol → candle list

def on_message(ws, message):
    msg = json.loads(message)
    if "topic" not in msg:
        return

    topic = msg["topic"]
    data = msg["data"][0]

    if not data["confirm"]:
        return  # Ignore incomplete candles

    symbol = topic.split(".")[2]
    candle_data[symbol].append({
        "time": data["start"],
        "high": float(data["high"]),
        "low": float(data["low"]),
    })

    # Keep last 50 candles per symbol
    if len(candle_data[symbol]) > 50:
        candle_data[symbol] = candle_data[symbol][-50:]

def on_open(ws):
    print("✅ Connected to Bybit WebSocket")
    for symbol in symbol_list:
        msg = {
            "op": "subscribe",
            "args": [f"kline.{interval}.{symbol}"]
        }
        ws.send(json.dumps(msg))
        print(f"📡 Subscribed: {symbol}")

def start_websocket():
    def run():
        while True:
            try:
                ws = websocket.WebSocketApp(
                    "wss://stream.bybit.com/v5/public/linear",
                    on_open=on_open,
                    on_message=on_message
                )
                ws.run_forever()
            except Exception as e:
                print("⚠️ Reconnecting in 5 seconds:", e)
                time.sleep(5)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
