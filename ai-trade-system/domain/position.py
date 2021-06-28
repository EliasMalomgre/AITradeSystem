import logging
from datetime import datetime

from mongoengine import Document, StringField, ListField, FloatField, BooleanField, DictField

from domain.position_status import PositionStatus
from domain.transaction_action import TransactionAction
from domain.transaction_log import TransactionLog
from properties.properties import Properties


class Position(Document):
    stock_name = StringField()
    frequency = StringField()
    current_transactions = ListField(default=[TransactionLog])
    current_amount = FloatField(default=0)
    total_buy_price = FloatField(default=0)
    average_buy_price = FloatField(default=0)
    p_and_l = FloatField(default=0)
    realized_p_and_l = FloatField(default=0)
    stop_loss = DictField(default=dict)
    risk = FloatField(default=Properties().risk)
    current_share_price = FloatField(default=0)
    open = BooleanField()
    position_size = FloatField(default=0)

    def process_transaction(self, transaction: TransactionLog):
        """Processes an incoming transaction"""
        if str(transaction.action) == str(TransactionAction.BUY):
            self.process_buy_transaction(transaction)
        elif str(transaction.action) == str(TransactionAction.SELL):
            self.process_sell_transaction(transaction)
        elif str(transaction.action) == str(TransactionAction.COVER):
            self.process_cover_transaction(transaction)
        elif str(transaction.action) == str(TransactionAction.SHORT):
            self.process_short_transaction(transaction)
        else:
            logging.warning("Tried adding transaction: {} but TransactionAction was incorrect", transaction)

    def process_buy_transaction(self, transaction: TransactionLog):
        """Processes an incoming buy transaction"""
        self.current_amount += transaction.amount
        self.total_buy_price += transaction.price_per_share * transaction.amount
        self.current_share_price = transaction.price_per_share
        self.update_average_buy_price()
        self.update_p_and_l()

    def process_sell_transaction(self, transaction: TransactionLog):
        """Processes an incoming sell transaction"""
        self.current_amount -= transaction.amount
        self.total_buy_price -= self.average_buy_price * transaction.amount
        self.current_share_price = transaction.price_per_share
        self.update_average_buy_price()
        self.update_p_and_l()

    def process_cover_transaction(self, transaction: TransactionLog):
        """Processes an incoming cover transaction"""
        self.current_amount += transaction.amount
        self.total_buy_price -= self.average_buy_price * transaction.amount
        self.current_share_price = transaction.price_per_share
        self.update_average_buy_price()
        self.update_p_and_l()

    def process_short_transaction(self, transaction: TransactionLog):
        """Processes an incoming short transaction"""
        self.current_amount -= transaction.amount
        self.total_buy_price += transaction.price_per_share * transaction.amount
        self.current_share_price = transaction.price_per_share
        self.update_average_buy_price()
        self.update_p_and_l()

    def update_average_buy_price(self):
        """Updates the average buy price"""
        if self.current_amount == 0:
            self.average_buy_price = 0
        elif self.current_amount > 0:
            self.average_buy_price = self.total_buy_price / self.current_amount
        else:
            self.average_buy_price = -self.total_buy_price / self.current_amount

    def update_p_and_l(self):
        """Updates the P&L"""
        self.p_and_l = (self.current_share_price - self.average_buy_price) * self.current_amount
        self.position_size = self.total_buy_price + self.p_and_l

    def get_stop_loss(self, date: datetime):
        """Returns the stop loss for the given date"""
        if date.strftime("%Y-%m-%d") in self.stop_loss:
            return self.stop_loss[date.strftime("%Y-%m-%d")]
        else:
            return 0

    def add_stop_loss(self, date: datetime, stop_loss):
        """Adds a stop loss value to the position"""
        self.stop_loss[date.strftime("%Y-%m-%d")] = stop_loss

    def get_status(self):
        """Returns the status of the position"""
        if self.current_amount > 0:
            return PositionStatus.LONG
        elif self.current_amount < 0:
            return PositionStatus.SHORT
        else:
            return PositionStatus.NONE

    def hit_stop_loss(self, previous_date: datetime, low, high):
        """Checks if the stop loss has been hit"""
        status = self.get_status()
        if status == PositionStatus.LONG:
            # Checks if there is a value for the incoming date
            # Checks if the low was smaller or equal to the stop loss value
            return previous_date.strftime("%Y-%m-%d") in self.stop_loss \
                   and low <= self.stop_loss[previous_date.strftime("%Y-%m-%d")]
        elif status == PositionStatus.SHORT:
            # Checks if there is a value for the incoming date
            # Checks if the high was greater or equal to the stop loss value
            return previous_date.strftime("%Y-%m-%d") in self.stop_loss \
                   and high >= self.stop_loss[previous_date.strftime("%Y-%m-%d")]
