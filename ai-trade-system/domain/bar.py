class Bar:
    def __init__(self, date, open, high, low, close, adj_close, volume, current_amount, stop_loss):
        # Stock information
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.adj_close = adj_close
        self.volume = volume

        # Postion information
        self.current_amount = current_amount
        # Latest value
        self.stop_loss = stop_loss

    def to_array(self):
        """Creates an array of all attributes needed as input for the AI"""
        return [self.open, self.high, self.low, self.adj_close,
                self.current_amount, self.stop_loss]
