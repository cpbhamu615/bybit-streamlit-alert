import streamlit as st
from bybit_stream import candle_data, start_websocket
from chart import plot_candles
from datetime import datetime
import pytz
import time

st.set_page_config(page_title="Crypto Candle Alert", layout="centered")
st.title("📈 Real-Time Crypto Candle Monitor")

st.markdown("### 💰 Live Prices")

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

# Start WebSocket (once)
if 'ws_started' not in st.session_state:
    start_websocket(symbols)
    st.session_state.ws_started = True

# Display live prices
prices = []
for sym in symbols:
    latest = candle_data.get(sym, [])
    if latest:
        price = float(latest[-1]["close"])
        prices.append((sym, price))
        st.write(f"**{sym}**: {price}")
    else:
        st.write(f"**{sym}**: Loading...")

# ✅ Correct timezone string
now = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S")
st.markdown(f"### ⏰ Live Time: {now}")

# Alert system
st.markdown("### 🔔 Alerts")

for sym in symbols:
    candles = candle_data.get(sym, [])
    if len(candles) < 4:
        continue

    ref = candles[-4]
    next_3 = candles[-3:]   # ✅ Correct line here

    high = float(ref["high"])
    low = float(ref["low"])

    all_inside = all(low <= float(c["low"]) and float(c["high"]) <= high for c in next_3)

    if all_inside:
        ts = datetime.fromtimestamp(ref["start"] / 1000, pytz.timezone("Asia/Kolkata"))
        st.warning(
            f"{sym} ALERT: 3 candles stayed inside range of {ts.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"High: {high} | Low: {low}"
        )

    st.markdown(f"#### 📊 {sym} Chart")
    fig = plot_candles(sym, ref)
    st.pyplot(fig)
