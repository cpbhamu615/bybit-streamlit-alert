import streamlit as st
import time
from bybit_stream import candle_data, start_websocket

st.set_page_config(page_title="Crypto Live Monitor", layout="wide")
st.title("📊 Live Bybit Crypto Monitor")

start_websocket()

st.markdown("### 💰 Live Prices (updated every second)")

# Live price display area
price_placeholder = st.empty()

st.markdown("---")
st.markdown("### 📡 Alert Section (3-minute candle logic)")

# Alert display area
alert_placeholder = st.empty()

def check_conditions(symbol):
    data = candle_data.get(symbol, [])
    if len(data) < 4:
        return None

    latest_idx = -4  # pick 4th last closed candle
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

while True:
    time.sleep(1)

    # ---- Show Live Prices ----
    live_prices = ""
    for sym in ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]:
        candles = candle_data.get(sym, [])
        if candles:
            last_close = candles[-1]["close"]
            live_prices += f"**{sym}**: {last_close}\n\n"
        else:
            live_prices += f"**{sym}**: waiting...\n\n"

    price_placeholder.markdown(live_prices)

    # ---- Check & Show Alerts ----
    alerts = []
    for sym in ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]:
        result = check_conditions(sym)
        if result:
            alerts.append(result)

    with alert_placeholder.container():
        if alerts:
            for alert in alerts:
                st.error(f"🔔 ALERT: {alert['symbol']} stayed inside candle from {alert['ref_time']} "
                         f"High: {alert['high']} | Low: {alert['low']}")
        else:
            st.info("⏳ No alert at the moment.")
