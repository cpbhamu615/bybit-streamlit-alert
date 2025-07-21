# data_buffer.py

from collections import defaultdict

# Store candle data for each symbol
candle_data = defaultdict(list)

def update_candles(symbol, new_candle):
    data = candle_data[symbol]

    # Check if it's a new candle or update existing
    if data and data[-1]["start"] == new_candle["start"]:
        data[-1] = new_candle
    else:
        data.append(new_candle)

    # Keep only last 100 candles
    if len(data) > 100:
        data.pop(0)
