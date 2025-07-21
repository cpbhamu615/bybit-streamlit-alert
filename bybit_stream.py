import asyncio
import websockets
import json
from data_buffer import candle_buffer

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

async def bybit_websocket():
    url = "wss://stream.bybit.com/v5/public/linear"

    async with websockets.connect(url) as ws:
        args = [f"kline.3.{symbol}" for symbol in symbols]

        await ws.send(json.dumps({
            "op": "subscribe",
            "args": args
        }))

        print("Subscribed to:", args)

        while True:
            msg = await ws.recv()
            data = json.loads(msg)

            if data.get("topic", "").startswith("kline.3."):
                topic = data["topic"]
                symbol = topic.split(".")[-1]
                candle = data["data"]
                
                if candle["confirm"]:
                    candle_data = {
                        "symbol": symbol,
                        "timestamp": candle["start"].split("T")[1][:5],  # HH:MM format
                        "open": float(candle["open"]),
                        "high": float(candle["high"]),
                        "low": float(candle["low"]),
                        "close": float(candle["close"]),
                    }
                    candle_buffer.add_candle(symbol, candle_data)
