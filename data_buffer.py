# data_buffer.py
import threading

class CandleBuffer:
    def __init__(self):
        self.lock = threading.Lock()
        self.candles = []

    def add_candle(self, candle):
        with self.lock:
            self.candles.append(candle)
            if len(self.candles) > 100:  # store latest 100 candles
                self.candles.pop(0)

    def get_candles(self):
        with self.lock:
            return list(self.candles)

candle_buffer = CandleBuffer()
