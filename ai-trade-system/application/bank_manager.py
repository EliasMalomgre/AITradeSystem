import datetime
import logging

from application.static_declarations import create_transaction_log, create_position
from domain.position import Position
from domain.share_entry import ShareEntry
from domain.transaction_action import TransactionAction
from domain.transaction_log import TransactionLog
from domain.wallet import Wallet
from properties.properties import Properties
from repositories.transaction_repository import TransactionRepository


class BankManager:
    def __init__(self):
        self.properties: Properties = Properties()
        self.trans_repo: TransactionRepository = TransactionRepository()

    def buy_shares(self, wallet: Wallet, entry: ShareEntry, amount: int, date: datetime, position: Position = None):
        """Executes buy transaction"""

        # Create transaction log
        transaction: TransactionLog = create_transaction_log(TransactionAction.BUY, entry.open, amount, entry.name,
                                                             entry.freq, date)

        # If position is None get position
        if position is None:
            position: Position = self.check_position(wallet, transaction)

        # Save and proces transaction
        self.save_transaction(transaction, position)
        wallet.process_transaction(transaction, position)

        logging.debug(
            "{} share of {} on {} has been bought for {} per share for frequency {}".format(amount, entry.name, date,
                                                                                            entry.open,
                                                                                            entry.freq))

    def sell_shares(self, wallet: Wallet, entry: ShareEntry, amount: int, date: datetime, position: Position = None,
                    share_price=None):
        """Executes sell transaction"""
        # Create transaction log
        transaction: TransactionLog = create_transaction_log(TransactionAction.SELL, entry.open if share_price is None
        else share_price, amount, entry.name,
                                                             entry.freq, date)
        # If position is None get position
        if position is None:
            position: Position = self.check_position(wallet, transaction)

        # Save and proces transaction
        self.save_transaction(transaction, position)
        wallet.process_transaction(transaction, position)

        logging.debug(
            "{} share of {} on {} has been sold for {} per share for frequency {}".format(amount, entry.name, date,
                                                                                          entry.open,
                                                                                          entry.freq))

    def short_shares(self, wallet: Wallet, entry: ShareEntry, amount: int, date: datetime, position: Position = None):
        """Executes short transaction"""
        # Create transaction log
        transaction: TransactionLog = create_transaction_log(TransactionAction.SHORT, entry.open, amount, entry.name,
                                                             entry.freq, date)
        # If position is None get position
        if position is None:
            position: Position = self.check_position(wallet, transaction)

        # Save and proces transaction
        self.save_transaction(transaction, position)
        wallet.process_transaction(transaction, position)

        logging.debug(
            "{} share of {} on {} has been shorted for {} per share for frequency {}".format(amount, entry.name, date,
                                                                                             entry.open,
                                                                                             entry.freq))

    def cover_shares(self, wallet: Wallet, entry: ShareEntry, amount: int, date: datetime, position: Position = None,
                     share_price=None):
        """Executes cover transaction"""
        # Create transaction log
        transaction: TransactionLog = create_transaction_log(TransactionAction.COVER, entry.open if share_price is None
        else share_price, amount, entry.name,
                                                             entry.freq, date)
        # If position is None get position
        if position is None:
            position: Position = self.check_position(wallet, transaction)

        # Save and proces transaction
        self.save_transaction(transaction, position)
        wallet.process_transaction(transaction, position)

        logging.debug(
            "{} share of {} on {} has been covered for {} per share for frequency {}".format(amount, entry.name, date,
                                                                                             entry.open,
                                                                                             entry.freq))

    def check_position(self, wallet: Wallet, transaction: TransactionLog):
        """Checks for a existing position and creates a new one when none are found"""
        try:
            return next(filter(lambda x: x.default_stock_name == transaction.stock_name and \
                                         str(x.frequency) == str(transaction.frequency) and x.open,
                               wallet.positions))
        except:
            return self.trans_repo.create_position(wallet,
                                                   create_position(transaction.stock_name, transaction.frequency))

    def save_transaction(self, transaction: TransactionLog, position: Position):
        """Saves transaction when configured"""
        if self.properties.agent_save_training_sessions:
            self.trans_repo.save_transaction(transaction, position)
