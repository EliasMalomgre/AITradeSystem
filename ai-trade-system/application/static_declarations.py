from datetime import datetime

from domain.frequency import Frequency
from domain.position import Position
from domain.transaction_action import TransactionAction
from domain.transaction_log import TransactionLog
from properties.properties import Properties


def create_transaction_log(action: TransactionAction, price_per_share: float, amount: int, stock_name: str,
                           frequency: Frequency,
                           timestamp: datetime = None):
    return TransactionLog(action=str(action), price_per_share=price_per_share, amount=amount, stock_name=stock_name,
                          frequency=str(frequency), time_stamp=timestamp)


def create_position(stock_name: str, frequency: Frequency, current_transactions: [TransactionLog] = [],
                    current_amount: float = 0,
                    total_buy_price: float = 0, average_buy_price: float = 0, p_and_l: float = 0, stop_loss=None,
                    risk: float = Properties().risk,
                    current_share_price: float = 0, open: bool = True):
    if stop_loss is None:
        stop_loss = {}
    return Position(stock_name=stock_name, frequency=str(frequency), current_transactions=current_transactions,
                    current_amount=current_amount,
                    total_buy_price=total_buy_price, average_buy_price=average_buy_price, p_and_l=p_and_l,
                    stop_loss=stop_loss, risk=risk,
                    current_share_price=current_share_price,
                    open=open)
