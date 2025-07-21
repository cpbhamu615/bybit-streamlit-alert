# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import threading
import time
from data_buffer import candle_buffer
from bybit_stream import start_websocket

st.set_page_config(page_title="Live Bybit Alert", layout="wide")
st.title("📡 Bybit 3-min Candle Breakout Alert")

# Start WebSocket thread
if 'started' not in st.session_state:
    thread = threading.Thread(target=start_websocket)
    thread.start()
    st.session_state.started = True
    st.success("🚀 Live data stream started!")

# Poll data every few seconds
time.sleep(1)
data = candle_buffer.get_candles()

if len(data) >= 4:
    df = pd.DataFrame(data)
    alerts = []
    i = 0
    while i + 3 < len(df):
        ref = df.iloc[i]
        next3 = df.iloc[i+1:i+4]

        if all((next3['high'] < ref['high']) & (next3['low'] > ref['low'])):
            alerts.append(f"🔔 ALERT: No break after candle {ref['timestamp']}")
            i += 4
        else:
            for j in range(1, 4):
                if df.iloc[i+j]['high'] >= ref['high'] or df.iloc[i+j]['low'] <= ref['low']:
                    i += j
                    break

    # Plot
    fig = go.Figure(data=[
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close']
        )
    ])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🚨 Alerts")
    for alert in alerts[-5:]:
        st.warning(alert)
else:
    st.info("⌛ Waiting for enough confirmed candles (need at least 4)...")
