from collections import defaultdict, deque

# Dictionary to store latest candles for each symbol
candle_data = defaultdict(lambda: deque(maxlen=100))
