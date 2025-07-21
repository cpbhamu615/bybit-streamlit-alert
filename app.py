# app.py
import streamlit as st
import time
from bybit_stream import candle_data, start_websocket
from datetime import datetime

st.set_page_config(page_title="Crypto Alert Scanner", layout="centered")
st.title("📈 Live Crypto Alert Scanner (3-min candles)")

# Start WebSocket background
start_websocket()

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
selected_symbol = st.selectbox("🪙 Select Crypto", SYMBOLS)

placeholder = st.empty()

def check_alert(candles):
    if len(candles) < 4:
        return None

    base = candles[-4]  # Candle to mark high/low from
    check1 = candles[-3]
    check2 = candles[-2]
    check3 = candles[-1]

    for c in [check1, check2, check3]:
        if c["high"] > base["high"] or c["low"] < base["low"]:
            return None  # No alert if broken

    return base

while True:
    candles = candle_data[selected_symbol]

    with placeholder.container():
        st.subheader(f"Live Scan: {selected_symbol}")
        st.write(f"🕒 Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        st.write(f"🕯️ Last candles received: {len(candles)}")

        if len(candles) >= 4:
            alert = check_alert(candles)
            if alert:
                st.error(f"🚨 Alert! Last 3 candles failed to break High/Low of candle at {datetime.utcfromtimestamp(alert['time']/1000).strftime('%H:%M')} UTC")
            else:
                st.success("✅ No valid alert yet")

        st.line_chart([c["high"] for c in candles[-20:]])

    time.sleep(5)
