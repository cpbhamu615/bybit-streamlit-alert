import streamlit as st
from datetime import datetime
import pytz
import pandas as pd
from bybit_stream import candle_data, prices
import time

st.set_page_config(layout="wide")
st.title("📈 Real-Time Crypto Candle Monitor")

# Indian Time
now = datetime.now(pytz.timezone("Asia/Kolkata"))
st.write(f"⏰ Current Time: {now.strftime('%H:%M:%S')}")

# Live Prices
st.subheader("💰 Live Prices")
for symbol, price in prices.items():
    st.write(f"{symbol}: {price}")

# Tabular Alert Section
st.subheader("🔔 Alerts")
for symbol, candles in candle_data.items():
    if len(candles) >= 4:
        selected = candles[-4]
        c1, c2, c3 = candles[-3], candles[-2], candles[-1]
        selected_time = datetime.fromtimestamp(selected['timestamp'], pytz.timezone("Asia/Kolkata")).strftime("%H:%M")
        rows = [{
            "Name": symbol,
            "selected candle time": selected_time,
            "High": selected["high"],
            "Low": selected["low"],
            "1st candle High": c1["high"], "1st candle Low": c1["low"],
            "2nd candle High": c2["high"], "2nd candle Low": c2["low"],
            "3rd candle High": c3["high"], "3rd candle Low": c3["low"],
            "Alert": "YES" if all(selected["low"] <= c["low"] <= selected["high"] and selected["low"] <= c["high"] <= selected["high"] for c in [c1, c2, c3]) else "NO"
        }]
        df = pd.DataFrame(rows)
        st.table(df)

# Auto Refresh Every 5 Seconds
time.sleep(5)
st.experimental_rerun()
