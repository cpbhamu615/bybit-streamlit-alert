from collections import defaultdict, deque

class CandleBuffer:
    def __init__(self, size=50):
        self.buffer = defaultdict(lambda: deque(maxlen=size))

    def add_candle(self, symbol, candle):
        self.buffer[symbol].append(candle)

    def get_candles(self, symbol):
        return list(self.buffer[symbol])

candle_buffer = CandleBuffer()
