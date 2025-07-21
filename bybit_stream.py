# bybit_stream.py
import asyncio
import websockets
import json
from datetime import datetime
from data_buffer import candle_buffer

async def bybit_stream():
    url = "wss://stream.bybit.com/v5/public/linear"
    symbol = "BTCUSDT"
    interval = "3"

    async with websockets.connect(url) as ws:
        subscribe_msg = {
            "op": "subscribe",
            "args": [f"kline.{interval}.{symbol}"]
        }
        await ws.send(json.dumps(subscribe_msg))
        print("✅ Subscribed to Bybit Kline")

        while True:
            msg = await ws.recv()
            data = json.loads(msg)

            if "data" in data and isinstance(data["data"], list):
                kline = data["data"][0]["kline"]
                if kline["confirm"]:
                    candle = {
                        "timestamp": datetime.fromtimestamp(kline["start"] / 1000).strftime("%H:%M"),
                        "open": float(kline["open"]),
                        "high": float(kline["high"]),
                        "low": float(kline["low"]),
                        "close": float(kline["close"])
                    }
                    candle_buffer.add_candle(candle)
                    print("✅ Confirmed candle added:", candle)

# Thread starter for Streamlit
def start_websocket():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bybit_stream())
