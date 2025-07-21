# app.py

import streamlit as st
import time
from datetime import datetime
import pytz
from bybit_stream import candle_data, prices, start_websocket
from data_buffer import buffer
import plotly.graph_objs as go

st.set_page_config(layout="wide")

if 'ws_started' not in st.session_state:
    start_websocket()
    st.session_state.ws_started = True

st.title("📈 Real-Time Crypto Candle Monitor")

# Live Prices
st.subheader("💰 Live Prices")
for symbol in ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]:
    price = prices.get(symbol, "Fetching...")
    st.write(f"{symbol}: {price}")

# Live Time
tz = pytz.timezone("Asia/Kolkata")
now = datetime.now(tz)
st.write(f"⏰ Live Time: {now.strftime('%H:%M:%S')}")

# Alerts
st.subheader("🔔 Alerts")
for symbol, candles in candle_data.items():
    if len(candles) >= 3:
        first = candles[-3]
        next_2 = candles[-2:]
        inside_range = all(first['low'] <= c['low'] <= first['high'] and first['low'] <= c['high'] <= first['high'] for c in next_2)
        if inside_range:
            t = datetime.fromtimestamp(first['start'] / 1000, tz).strftime('%Y-%m-%d %H:%M:%S')
            st.warning(f"{symbol} ALERT: 3 candles stayed inside range of {t} | High: {first['high']} | Low: {first['low']}")

# Charts
st.subheader("📊 Candlestick Charts")
for symbol, candles in candle_data.items():
    if len(candles) >= 3:
        fig = go.Figure(data=[go.Candlestick(
            x=[datetime.fromtimestamp(c['start'] / 1000, tz) for c in candles],
            open=[float(c['open']) for c in candles],
            high=[float(c['high']) for c in candles],
            low=[float(c['low']) for c in candles],
            close=[float(c['close']) for c in candles],
        )])
        fig.update_layout(title=f"{symbol} - 3-min Candles", xaxis_title="Time", yaxis_title="Price", height=400)
        st.plotly_chart(fig, use_container_width=True)

# Refresh every 10 seconds
st.experimental_rerun()
time.sleep(10)
