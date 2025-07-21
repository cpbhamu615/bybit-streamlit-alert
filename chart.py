import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pytz
from data_buffer import candle_data

def plot_candles(symbol, ref_candle):
    candles = candle_data.get(symbol, [])
    if len(candles) < 10:
        return plt.figure()

    times = []
    opens = []
    highs = []
    lows = []
    closes = []

    for c in list(candles)[-20:]:
        dt = datetime.fromtimestamp(c["start"] / 1000, pytz.timezone("Asia/Kolkata"))
        times.append(dt)
        opens.append(float(c["open"]))
        highs.append(float(c["high"]))
        lows.append(float(c["low"]))
        closes.append(float(c["close"]))

    fig, ax = plt.subplots(figsize=(6, 3))
    for i in range(len(times)):
        color = 'green' if closes[i] >= opens[i] else 'red'
        ax.plot([times[i], times[i]], [lows[i], highs[i]], color=color)
        ax.plot([times[i], times[i]], [opens[i], closes[i]], color=color, linewidth=4)

    # Highlight reference candle
    ref_start = datetime.fromtimestamp(ref_candle["start"] / 1000, pytz.timezone("Asia/Kolkata"))
    ref_end = datetime.fromtimestamp(ref_candle["end"] / 1000, pytz.timezone("Asia/Kolkata"))
    ax.axhline(float(ref_candle["high"]), color='blue', linestyle='--', linewidth=1)
    ax.axhline(float(ref_candle["low"]), color='blue', linestyle='--', linewidth=1)
    ax.set_title(f"{symbol} - 3min Candle Chart")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.autofmt_xdate()
    return fig
