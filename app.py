**# app.py**
import streamlit as st
import time
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
from bybit_stream import candle_data, start_websocket

st.set_page_config(layout="wide")
st.title("\ud83d\udcc8 Real-Time Crypto Candle Monitor")

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
REFRESH_INTERVAL = 10

if "websocket_started" not in st.session_state:
    start_websocket()
    st.session_state.websocket_started = True

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > REFRESH_INTERVAL:
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()

st.subheader("\ud83d\udcb0 Live Prices")
for sym in symbols:
    candles = candle_data.get(sym, [])
    if candles:
        st.markdown(f"**{sym}**: {candles[-1]['close']}")

now = datetime.now(pytz.timezone("Asia/Kolkata"))
st.write(f"\u23f0 Live Time: {now.strftime('%H:%M:%S')}")

def plot_candles(symbol, candle):
    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    o = float(candle["open"])
    h = float(candle["high"])
    l = float(candle["low"])
    c = float(candle["close"])
    color = "green" if c >= o else "red"
    ax.plot([1, 1], [l, h], color="black")
    ax.bar(1, abs(c - o), bottom=min(o, c), width=0.5, color=color)
    ax.set_xticks([])
    ax.set_title(symbol)
    return fig

st.subheader("\ud83d\udd14 Alerts")
for sym in symbols:
    candles = candle_data.get(sym)

    if not isinstance(candles, list) or len(candles) < 4:
        continue

    ref = candles[-4]
    next_3 = candles[-3:]

    high = float(ref["high"])
    low = float(ref["low"])

    all_inside = all(
        low <= float(c["low"]) and float(c["high"]) <= high for c in next_3
    )

    if all_inside:
        ts = datetime.fromtimestamp(ref["start"] / 1000, pytz.timezone("Asia/Kolkata"))
        st.warning(
            f"{sym} ALERT: 3 candles stayed inside range of {ts.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"High: {high} | Low: {low}"
        )

    st.markdown(f"#### \ud83d\udcca {sym} Chart")
    fig = plot_candles(sym, ref)
    st.pyplot(fig)


**# bybit_stream.py**
import websocket
import json
import threading
from data_buffer import candle_data

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

ws_url = "wss://stream.bybit.com/v5/public/linear"


def on_message(ws, message):
    msg = json.loads(message)
    if msg.get("topic") and "kline" in msg["topic"]:
        data = msg["data"]
        symbol = data["symbol"]
        candle_data.setdefault(symbol, []).append(data)
        if len(candle_data[symbol]) > 100:
            candle_data[symbol] = candle_data[symbol][-100:]


def on_open(ws):
    print("WebSocket opened")
    for sym in symbols:
        sub_msg = {
            "op": "subscribe",
            "args": [f"kline.3.{sym}"]
        }
        ws.send(json.dumps(sub_msg))


def run_websocket():
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message
    )
    ws.run_forever()


def start_websocket():
    t = threading.Thread(target=run_websocket)
    t.daemon = True
    t.start()


**# data_buffer.py**
candle_data = {}
