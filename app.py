# app.py

import streamlit as st
import time
from bybit_stream import candle_data, start_websocket

st.set_page_config(page_title="Crypto Alert", layout="wide")
st.title("📈 Bybit Live Crypto Alert App")

start_websocket()

def check_conditions(symbol):
    data = candle_data.get(symbol, [])
    if len(data) < 4:
        return None

    latest_idx = -4  # select 4th last closed candle
    ref_candle = data[latest_idx]
    next_candles = data[latest_idx+1:latest_idx+4]

    high = ref_candle["high"]
    low = ref_candle["low"]

    all_within_range = all(
        c["high"] <= high and c["low"] >= low for c in next_candles
    )

    if all_within_range:
        return {
            "symbol": symbol,
            "ref_time": ref_candle["timestamp"],
            "high": high,
            "low": low
        }

    return None

st.markdown("Live monitoring on 3-minute candles for BTC, ETH, BNB, SOL")

placeholder = st.empty()

while True:
    time.sleep(1)
    alerts = []
    for sym in ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]:
        result = check_conditions(sym)
        if result:
            alerts.append(result)

    with placeholder.container():
        if alerts:
            for alert in alerts:
                st.error(f"🔔 ALERT: {alert['symbol']} stayed inside candle from {alert['ref_time']} "
                         f"High: {alert['high']} | Low: {alert['low']}")
        else:
            st.success("✅ Monitoring... No alert yet.")
