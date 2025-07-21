# app.py

import streamlit as st
from datetime import datetime
import pytz
from bybit_stream import candle_data, start_websocket
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(layout="wide")
st.title("📈 Real-Time Crypto Candle Monitor")

# Start WebSocket only once
if "websocket_started" not in st.session_state:
    start_websocket()
    st.session_state.websocket_started = True

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

st.subheader("💰 Live Prices")

# Show latest price
for sym in symbols:
    data = candle_data.get(sym, [])
    if data:
        last = data[-1]
        st.write(f"**{sym}**: {last['close']}")

# Live Time
now = datetime.now(pytz.timezone("Asia/Kolkata"))
st.write(f"⏰ Live Time: {now.strftime('%H:%M:%S')}")

st.subheader("🔔 Alerts")

# Alert logic + chart plotting
def plot_candles(symbol, candle):
    fig, ax = plt.subplots(figsize=(4, 2))
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

    st.markdown(f"#### 📊 {sym} Chart")
    fig = plot_candles(sym, ref)
    st.pyplot(fig)
