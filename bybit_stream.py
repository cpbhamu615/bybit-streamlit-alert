import asyncio
import websockets
import json

async def test_connection():
    url = "wss://stream.bybit.com/v5/public/linear"

    async with websockets.connect(url) as ws:
        print("✅ Connected to Bybit WebSocket")

        subscribe_msg = {
            "op": "subscribe",
            "args": ["kline.3.BTCUSDT"]
        }
        await ws.send(json.dumps(subscribe_msg))
        print("📡 Subscription message sent")

        while True:
            msg = await ws.recv()
            print("📨 Message received:")
            print(msg)

asyncio.run(test_connection())
