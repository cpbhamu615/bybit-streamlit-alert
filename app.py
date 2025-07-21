import streamlit as st
import time
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go

from bybit_stream import candle_data, start_websocket

# Page Setup
st.set_page_config(page_title="Crypto Live Tracker", layout="wide")
st.title("📈 Real-Time Crypto Candle Monitor")

# Start WebSocket
start_websocket()

# UI placeholders
col1, col2 = st.columns(2)
price_placeholder = col1.empty()
time_placeholder = col2.empty()

chart_placeholder = st.empty()
alert_placeholder = st.empty()

# Crypto symbols
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]

def check_conditions(symbol):
    data = candle_data.get(symbol, [])
    if len(data) < 4:
        return None

    idx = -4  # 4th last candle (completed one)
    ref_candle = data[idx]
    next_3 = data[idx+1:idx+4]

    high = ref_candle["high"]
    low = ref_candle["low"]

    all_inside = all(c["high"] <= high and c["low"] >= low for c in next_3)

    if all_inside:
        return ref_candle
    return None

def plot_candles(symbol, ref_candle):
    data = candle_data.get(symbol, [])
    if not data or len(data) < 10:
        return None

    df = pd.DataFrame(data[-10:])  # Last 10 candles
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
    fig = go.Figure(data=[go.Candlestick(
        x=df["timestamp"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    fig.update_layout(title=f"{symbol} - Last 10 Candles", xaxis_title="Time", yaxis_title="Price")
    return fig

while True:
    time.sleep(1)

    # 1️⃣ Show Live Prices
    prices_text = "### 💰 **Live Prices**\n\n"
    for sym in symbols:
        last_candle = candle_data.get(sym, [])
        if last_candle:
            prices_text += f"**{sym}**: {last_candle[-1]['close']}\n\n"
        else:
            prices_text += f"**{sym}**: Loading...\n\n"
    price_placeholder.markdown(prices_text)

    # 2️⃣ Show Current System Time
    now = datetime.now().strftime("%H:%M:%S")
    time_placeholder.markdown(f"### ⏰ **Live Time**: {now}")

    # 3️⃣ Show Alerts with Chart
    for sym in symbols:
        ref = check_conditions(sym)
        if ref:
            ref_time = datetime.fromtimestamp(ref["timestamp"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            alert_placeholder.warning(f"🔔 **{sym} ALERT**: 3 candles stayed inside range of {ref_time} | "
                                      f"High: {ref['high']} | Low: {ref['low']}")

            # 4️⃣ Show Chart
            fig = plot_candles_
