class Action:
    def __init__(self, stop_loss: float = 0.0, buy: float = 0, sell: float = 0,
                 short: float = 0, cover: float = 0):
        self.stop_loss: float = stop_loss
        self.buy = buy
        self.sell = sell
        self.short = short
        self.cover = cover
