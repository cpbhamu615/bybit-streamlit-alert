import asyncio
import websockets
import json
from datetime import datetime

async def bybit_candle_stream():
    url = "wss://stream.bybit.com/v5/public/linear"  # For USDT Perpetual
    symbol = "BTCUSDT"
    interval = "3"

    async with websockets.connect(url) as ws:
        # Subscribe to 3m candle stream
        subscribe_msg = {
            "op": "subscribe",
            "args": [f"kline.{interval}.{symbol}"]
        }
        await ws.send(json.dumps(subscribe_msg))

        while True:
            response = await ws.recv()
            data = json.loads(response)

            if "data" in data and "kline" in data["data"]:
                kline = data["data"]["kline"]
                candle = {
                    "timestamp": datetime.fromtimestamp(kline["start"] / 1000).strftime("%H:%M"),
                    "open": float(kline["open"]),
                    "high": float(kline["high"]),
                    "low": float(kline["low"]),
                    "close": float(kline["close"])
                }
                print("LIVE CANDLE:", candle)

# Run directly (for testing)
if __name__ == "__main__":
    asyncio.run(bybit_candle_stream())
