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

# Show Indian time
now = datetime.now(pytz.timezone("Asia/Kolka
