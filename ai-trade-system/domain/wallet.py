from mongoengine import Document, FloatField, ListField

from domain.position import Position
from domain.transaction_action import TransactionAction
from domain.transaction_log import TransactionLog
from properties.properties import Properties


class Wallet(Document):
    balance = FloatField(default=25000)
    equity = FloatField(default=25000)
    buying_power = FloatField(default=100000)

    positions = ListField(default=[Position])

    properties: Properties = Properties()

    def process_transaction(self, transaction_log: TransactionLog, position: Position):
        """Processes an incoming transaction"""

        # If the transaction is a sell or cover update the equity
        if str(transaction_log.action) == str(TransactionAction.SELL):
            profit = transaction_log.amount * (transaction_log.price_per_share - position.average_buy_price)
            self.equity += profit
            position.realized_p_and_l += profit
        elif str(transaction_log.action) == str(TransactionAction.COVER):
            profit = transaction_log.amount * (position.average_buy_price - transaction_log.price_per_share)
            self.equity += profit
            position.realized_p_and_l += profit

        position.process_transaction(transaction_log)
        self.update_equity()

    def update_equity(self):
        self.balance = self.equity
        # Add all the P&L to the ablance
        for position in list(filter(lambda x: x.open, self.positions)):
            self.balance += position.p_and_l

        self.buying_power = (self.balance * self.properties.leverage)
        # Take of the position size of all positions
        for position in list(filter(lambda x: x.open, self.positions)):
            self.buying_power -= position.position_size
