import numpy as np

from domain.bar import Bar


class State:
    def __init__(self, buying_power, position_open, bars: [Bar] = None):
        self.bars = bars
        self.buying_power = buying_power
        self.position_open = position_open

    def to_array(self):
        """Creates an array of all attributes needed as input for the AI"""
        array = [self.buying_power, self.position_open]
        # Coverts all bars to arrays
        for bar in self.bars:
            array += bar.to_array()
        return np.asarray(array).astype(np.float32)
