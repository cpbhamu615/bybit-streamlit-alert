# bybit_stream.py

import websocket
import json
import threading

candle_data = {
    "BTCUSDT": [],
    "ETHUSDT": [],
    "BNBUSDT": [],
    "SOLUSDT": []
}

symbol_list = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

def on_message(ws, message):
    data = json.loads(message)
    topic = data.get("topic")
    if topic:
        symbol = topic.split(".")[-1]
        kline = data["data"][0]

        if kline["confirm"]:
            candle_data[symbol].append({
                "timestamp": kline["start"],
                "open": float(kline["open"]),
                "high": float(kline["high"]),
                "low": float(kline["low"]),
                "close": float(kline["close"])
            })

            # Limit to last 100 candles
            if len(candle_data[symbol]) > 100:
                candle_data[symbol] = candle_data[symbol][-100:]

def on_open(ws):
    print("✅ Connected to Bybit WebSocket")
    for symbol in symbol_list:
        payload = {
            "op": "subscribe",
            "args": [f"kline.3.{symbol}"]
        }
        ws.send(json.dumps(payload))

def on_error(ws, error):
    print("❌ WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("🔌 WebSocket closed")

def start_websocket():
    ws = websocket.WebSocketApp(
        "wss://stream.bybit.com/v5/public/linear",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()
