# app.py

import streamlit as st
import pandas as pd
import time
from datetime import datetime
import pytz
from data_buffer import candle_data, prices
from bybit_stream import start_websocket

# Setup
st.set_page_config(page_title="Crypto Monitor", layout="wide")
st.title("📈 Real-Time Crypto Candle Monitor")

# Start WebSocket once
if "started" not in st.session_state:
    start_websocket()
    st.session_state.started = True

# Show current Indian time
now = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%H:%M:%S")
st.markdown(f"⏰ Current Time: `{now}`")

# Show Live Prices
st.subheader("💰 Live Prices")
for sym in ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]:
    st.write(f"**{sym}:** {prices[sym]}")

# Process & show alerts
st.subheader("🔔 Alerts")
alerts = []

for sym, candles in candle_data.items():
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
                "Alert": "Yes ✅"
            })

if alerts:
    st.dataframe(pd.DataFrame(alerts), use_container_width=True)
else:
    st.info("No valid alerts yet.")

# Auto refresh every 5 seconds
countdown = st.empty()
for i in range(5, 0, -1):
    countdown.text(f"Refreshing in {i} seconds...")
    time.sleep(1)
st.rerun()
