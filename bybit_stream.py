# app.py

import streamlit as st
import time
from bybit_stream import candle_data, start_websocket

st.title("🚀 Live Multi-Crypto Alert System")

start_websocket()

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
selected_symbol = st.selectbox("Select Symbol", symbols)

placeholder = st.empty()

def check_alert(symbol):
    candles = candle_data.get(symbol, [])
    if len(candles) < 4:
        return None

    marked = candles[-4]
    next_3 = candles[-3:]

    high = marked["high"]
    low = marked["low"]

    for c in next_3:
        if c["high"] > high or c["low"] < low:
            return None
    return marked["time"]

while True:
    alert_time = check_alert(selected_symbol)
    if alert_time:
        placeholder.error(f"🚨 Alert: {selected_symbol} did NOT break {alert_time} high/low in next 3 candles!")
    time.sleep(5)
