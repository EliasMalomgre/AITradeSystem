from enum import Enum


class TransactionAction(Enum):
    BUY = "BUY"
    SELL = "SELL"
    SHORT = "SHORT"
    COVER = "COVER"
    NONE = "NONE"
