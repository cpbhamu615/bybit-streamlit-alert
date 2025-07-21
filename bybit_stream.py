import websocket
import json
import threading
from data_buffer import candle_data

def on_message(ws, message):
    data = json.loads(message)

    if "topic" in data and "data" in data:
        topic = data["topic"]
        if topic.startswith("kline.3."):
            symbol = topic.split(".")[2]
            for candle in data["data"]:
                candle_data[symbol].append(candle)

def on_open(ws):
    print("✅ Connected to Bybit WebSocket")
    subscribe_message = {
        "op": "subscribe",
        "args": [
            "kline.3.BTCUSDT",
            "kline.3.ETHUSDT",
            "kline.3.BNBUSDT",
            "kline.3.SOLUSDT"
        ]
    }
    ws.send(json.dumps(subscribe_message))
    print("📡 Subscription message sent")

def on_error(ws, error):
    print(f"❌ Error: {error}")

def on_close(ws):
    print("🔌 WebSocket closed")

def start_websocket(symbols):
    def run():
        ws = websocket.WebSocketApp(
            "wss://stream.bybit.com/v5/public/linear",
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.run_forever()

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
