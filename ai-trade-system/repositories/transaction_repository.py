from domain.position import Position
from domain.transaction_log import TransactionLog
from domain.wallet import Wallet
from properties.properties import Properties
from repositories.repository import Repository


class TransactionRepository(Repository):
    def __init__(self):
        super().__init__()
        self.properties: Properties = Properties()

    @staticmethod
    def get_wallet() -> Wallet:
        w: Wallet = Wallet.objects().first()
        if w is None:
            w = Wallet(equity=25000, positions=[])
        return w

    @staticmethod
    def get_stats_for_stock(stock_name: str):
        return Position.objects(stock_name=stock_name)

    def save_wallet(self, wallet: Wallet):
        pass

    def save_transaction(self, t: TransactionLog, p: Position):
        if self.properties.agent_save_training_sessions and t.id is not None:
            t.save()
        elif self.properties.agent_save_training_sessions:
            t.save()
            p.current_transactions.append(t)
            p.save()
        else:
            p.current_transactions.append(t)

    @staticmethod
    def get_transaction(_id) -> TransactionLog:
        t: TransactionLog = TransactionLog.objects(id=_id).first()
        return t

    @staticmethod
    def create_position(w: Wallet, p: Position) -> Position:
        p.save()
        w.positions.append(p)
        return p

    @staticmethod
    def save_position(p: Position):
        p.save()

    @staticmethod
    def get_position(_id) -> Position:
        p: Position = Position.objects(id=_id).first()
        return p
