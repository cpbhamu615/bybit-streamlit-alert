import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.title("🕵️ Crypto 3-min Candle Breakout Scanner")

# Data load
df = pd.read_csv("sample_3min_data.csv")

# Show table
st.subheader("📊 Candle Data")
st.dataframe(df)

# Marked candle logic
alerts = []

for i in range(len(df)-3):
    mark = df.iloc[i]
    next_3 = df.iloc[i+1:i+4]

    high = mark['high']
    low = mark['low']

    if all((next_3['high'] < high) & (next_3['low'] > low)):
        alerts.append(f"🔔 Alert: Candle at {mark['timestamp']} not broken in next 3 candles!")

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

# Show alerts
st.subheader("🚨 Alerts")
for alert in alerts:
    st.warning(alert)
