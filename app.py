# app.py

import streamlit as st
import time
from bybit_stream import candle_data, prices, start_websocket
from datetime import datetime
import pytz
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
start_websocket()

st.title("📈 Real-Time Crypto Candle Monitor")

# Auto refresh
st_autorefresh = st.empty()
REFRESH_INTERVAL = 3  # seconds

while True:
    st_autorefresh.empty()
    st_autorefresh = st.empty()

    with st_autorefresh.container():
        st.subheader("💰 Live Prices")
        for symbol in ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]:
            st.write(f"**{symbol}**: {prices.get(symbol, 'Loading...')}")

        now = datetime.now(pytz.timezone("Asia/Kolkata"))
        st.write(f"⏰ **Live Time (IST):** {now.strftime('%H:%M:%S')}")

        st.subheader("🔔 Alerts")

        for symbol in candle_data:
            candles = candle_data[symbol][-10:]
            if len(candles) >= 4:
                last = candles[-1]
                prev_3 = candles[-4:-1]

                high = float(last["high"])
                low = float(last["low"])
                inside_count = 0

                for c in prev_3:
                    if float(c["high"]) <= high and float(c["low"]) >= low:
                        inside_count += 1

                if inside_count == 3:
                    start_time = datetime.fromtimestamp(last["start"] / 1000, pytz.timezone("Asia/Kolkata"))
                    st.success(f"{symbol} ALERT: 3 candles stayed inside range of {start_time.strftime('%Y-%m-%d %H:%M:%S')} | High: {high} | Low: {low}")

        st.subheader("📊 Candle Chart (Last 10 candles)")
        selected_symbol = st.selectbox("Select Symbol", ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"])

        selected_data = candle_data[selected_symbol][-10:]
        if selected_data:
            df = pd.DataFrame(selected_data)
            df['timestamp'] = pd.to_datetime(df['start'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)

            fig = go.Figure(data=[go.Candlestick(
                x=df['timestamp'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']
            )])
            fig.update_layout(xaxis_rangeslider_visible=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

    time.sleep(REFRESH_INTERVAL)
