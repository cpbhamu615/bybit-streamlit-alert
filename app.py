# app.py

import streamlit as st
import pandas as pd
import time
from datetime import datetime
import pytz
from data_buffer import candle_data, prices
from bybit_stream import start_websocket

st.set_page_config(page_title="Crypto Live Monitor", layout="wide")
st.title("📈 Real-Time Crypto Candle Monitor")

if "started" not in st.session_state:
    start_websocket()
    st.session_state.started = True

# Time
now = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S")
st.markdown(f"⏰ Current Time: `{now}`")

# Prices
st.subheader("💰 Live Prices")
price_cols = st.columns(4)
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
for i, sym in enumerate(symbols):
    with price_cols[i]:
        st.metric(label=sym, value=prices[sym])

# Alerts Table
st.subheader("🔔 Alerts")
alerts = []
for sym in symbols:
    candles = candle_data[sym]
    if len(candles) >= 4:
        selected = candles[-4]
        next_3 = candles[-3:]
        high = selected["high"]
        low = selected["low"]
        inside = all(c["high"] <= high and c["low"] >= low for c in next_3)
        if inside:
            alerts.append({
                "Symbol": sym,
                "Time": datetime.fromtimestamp(selected["timestamp"], pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"),
                "High": high,
                "Low": low,
                "Status": "3 candles inside range ✅"
            })

if alerts:
    df = pd.DataFrame(alerts)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No alerts yet.")

# Auto-refresh
countdown = st.empty()
for i in range(5, 0, -1):
    countdown.text(f"Refreshing in {i} seconds...")
    time.sleep(1)
st.rerun()
