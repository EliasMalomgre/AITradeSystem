import unittest
from datetime import datetime

from application.bank_manager import BankManager
from application.static_declarations import create_position
from application.stock_simulator import StockSimulator
from domain.frequency import Frequency
from domain.position import Position
from domain.share_entry import ShareEntry
from domain.wallet import Wallet


class TransactionTest(unittest.TestCase):

    def setUp(self):
        self.wallet = Wallet()
        self.wallet.positions.pop(0)
        self.simulator = StockSimulator()
        self.manager = BankManager()
        position: Position = create_position("TEST", Frequency.ONE_DAY)
        self.wallet.positions.append(position)

    def test_buy_transaction(self):
        position: Position = self.wallet.positions[-1]

        self.manager.buy_shares(self.wallet,
                                ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                           open=50, high=50, low=50, close=50, adj_close=50, volume=10000), 100,
                                datetime.now, position)

        self.assertEqual(100, position.current_amount)
        self.assertEqual(5000, position.total_buy_price)
        self.assertEqual(50, position.current_share_price)
        self.assertEqual(50, position.average_buy_price)
        self.assertEqual(str(Frequency.ONE_DAY), str(position.frequency))
        self.assertEqual("TEST", position.stock_name)
        self.assertEqual(0, position.p_and_l)
        self.assertEqual(0, position.realized_p_and_l)
        self.assertEqual(5000, position.position_size)

        self.assertEqual(25000, self.wallet.balance)
        self.assertEqual(25000, self.wallet.equity)
        self.assertEqual(95000, self.wallet.buying_power)

    def test_sell_transaction(self):
        position: Position = self.wallet.positions[-1]

        self.manager.buy_shares(self.wallet,
                                ShareEntry(name="TEST", date=datetime(2019, 1, 1), freq=str(Frequency.ONE_DAY),
                                           open=50, high=50, low=50, close=50, adj_close=50, volume=10000), 100,
                                datetime.now, position)

        position.current_share_price = 75
        position.update_p_and_l()

        self.manager.sell_shares(self.wallet,
                                 ShareEntry(name="TEST", date=datetime(2019, 1, 2), freq=str(Frequency.ONE_DAY),
                                            open=75, high=50, low=50, close=50, adj_close=50, volume=10000), 50,
                                 datetime.now, position)

        self.assertEqual(50, position.current_amount)
        self.assertEqual(2500, position.total_buy_price)
        self.assertEqual(50, position.average_buy_price)
        self.assertEqual(str(Frequency.ONE_DAY), str(position.frequency))
        self.assertEqual("TEST", position.stock_name)
        self.assertEqual(1250, position.p_and_l)
        self.assertEqual(1250, position.realized_p_and_l)
        self.assertEqual(3750, position.position_size)

        self.assertEqual(27500, self.wallet.balance)
        self.assertEqual(26250, self.wallet.equity)
        self.assertEqual(106250, self.wallet.buying_power)

    def test_short_transaction(self):
        position: Position = self.wallet.positions[-1]

        self.manager.short_shares(self.wallet,
                                  ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                             open=50, high=50, low=50, close=50, adj_close=50, volume=10000), 100,
                                  datetime.now, position)

        self.assertEqual(-100, position.current_amount)
        self.assertEqual(5000, position.total_buy_price)
        self.assertEqual(50, position.current_share_price)
        self.assertEqual(50, position.average_buy_price)
        self.assertEqual(str(Frequency.ONE_DAY), str(position.frequency))
        self.assertEqual("TEST", position.stock_name)
        self.assertEqual(0, position.p_and_l)
        self.assertEqual(0, position.realized_p_and_l)
        self.assertEqual(5000, position.position_size)

        self.assertEqual(25000, self.wallet.balance)
        self.assertEqual(25000, self.wallet.equity)
        self.assertEqual(95000, self.wallet.buying_power)

    def test_cover_transaction(self):
        position: Position = self.wallet.positions[-1]

        self.manager.short_shares(self.wallet,
                                  ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                             open=50, high=50, low=50, close=50, adj_close=50, volume=10000), 100,
                                  datetime.now, position)

        self.manager.cover_shares(self.wallet,
                                  ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                             open=25, high=50, low=50, close=50, adj_close=50, volume=10000), 50,
                                  datetime.now, position)

        self.assertEqual(-50, position.current_amount)
        self.assertEqual(2500, position.total_buy_price)
        self.assertEqual(50, position.average_buy_price)
        self.assertEqual(str(Frequency.ONE_DAY), str(position.frequency))
        self.assertEqual("TEST", position.stock_name)
        self.assertEqual(1250, position.p_and_l)
        self.assertEqual(1250, position.realized_p_and_l)
        self.assertEqual(3750, position.position_size)

        self.assertEqual(27500, self.wallet.balance)
        self.assertEqual(26250, self.wallet.equity)
        self.assertEqual(106250, self.wallet.buying_power)

    def test_integration(self):
        position: Position = self.wallet.positions[-1]

        # Long
        self.manager.buy_shares(self.wallet,
                                ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                           open=50, high=50, low=50, close=50, adj_close=50, volume=10000), 100,
                                datetime.now, position)

        self.assertEqual(100, position.current_amount)
        self.assertEqual(5000, position.total_buy_price)
        self.assertEqual(50, position.current_share_price)
        self.assertEqual(50, position.average_buy_price)
        self.assertEqual(0, position.p_and_l)
        self.assertEqual(0, position.realized_p_and_l)
        self.assertEqual(5000, position.position_size)

        self.assertEqual(25000, self.wallet.balance)
        self.assertEqual(25000, self.wallet.equity)
        self.assertEqual(95000, self.wallet.buying_power)

        position.current_share_price = 75
        position.update_p_and_l()
        self.wallet.update_equity()

        self.assertEqual(100, position.current_amount)
        self.assertEqual(5000, position.total_buy_price)
        self.assertEqual(75, position.current_share_price)
        self.assertEqual(50, position.average_buy_price)
        self.assertEqual(2500, position.p_and_l)
        self.assertEqual(0, position.realized_p_and_l)
        self.assertEqual(7500, position.position_size)

        self.assertEqual(27500, self.wallet.balance)
        self.assertEqual(25000, self.wallet.equity)
        self.assertEqual(102500, self.wallet.buying_power)

        self.manager.buy_shares(self.wallet,
                                ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                           open=100, high=50, low=50, close=50, adj_close=50, volume=10000), 100,
                                datetime.now, position)

        self.assertEqual(200, position.current_amount)
        self.assertEqual(15000, position.total_buy_price)
        self.assertEqual(100, position.current_share_price)
        self.assertEqual(75, position.average_buy_price)
        self.assertEqual(5000, position.p_and_l)
        self.assertEqual(0, position.realized_p_and_l)
        self.assertEqual(20000, position.position_size)

        self.assertEqual(30000, self.wallet.balance)
        self.assertEqual(25000, self.wallet.equity)
        self.assertEqual(100000, self.wallet.buying_power)

        self.manager.sell_shares(self.wallet,
                                 ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                            open=200, high=50, low=50, close=50, adj_close=50, volume=10000), 200,
                                 datetime.now, position)

        self.assertEqual(0, position.current_amount)
        self.assertEqual(0, position.total_buy_price)
        self.assertEqual(200, position.current_share_price)
        self.assertEqual(0, position.average_buy_price)
        self.assertEqual(0, position.p_and_l)
        self.assertEqual(25000, position.realized_p_and_l)
        self.assertEqual(0, position.position_size)

        self.assertEqual(50000, self.wallet.balance)
        self.assertEqual(50000, self.wallet.equity)
        self.assertEqual(200000, self.wallet.buying_power)

        self.wallet.balance = 25000
        self.wallet.equity = 25000
        self.wallet.buying_power = 100000

        # Short
        self.manager.short_shares(self.wallet,
                                  ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                             open=50, high=50, low=50, close=50, adj_close=50, volume=10000), 100,
                                  datetime.now, position)

        self.assertEqual(-100, position.current_amount)
        self.assertEqual(5000, position.total_buy_price)
        self.assertEqual(50, position.current_share_price)
        self.assertEqual(50, position.average_buy_price)
        self.assertEqual(0, position.p_and_l)
        self.assertEqual(25000, position.realized_p_and_l)
        self.assertEqual(5000, position.position_size)

        self.assertEqual(25000, self.wallet.balance)
        self.assertEqual(25000, self.wallet.equity)
        self.assertEqual(95000, self.wallet.buying_power)

        position.current_share_price = 75
        position.update_p_and_l()
        self.wallet.update_equity()

        self.assertEqual(-100, position.current_amount)
        self.assertEqual(5000, position.total_buy_price)
        self.assertEqual(75, position.current_share_price)
        self.assertEqual(50, position.average_buy_price)
        self.assertEqual(-2500, position.p_and_l)
        self.assertEqual(25000, position.realized_p_and_l)
        self.assertEqual(2500, position.position_size)

        self.assertEqual(22500, self.wallet.balance)
        self.assertEqual(25000, self.wallet.equity)
        self.assertEqual(87500, self.wallet.buying_power)

        self.manager.short_shares(self.wallet,
                                  ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                             open=100, high=50, low=50, close=50, adj_close=50, volume=10000), 100,
                                  datetime.now, position)

        self.assertEqual(-200, position.current_amount)
        self.assertEqual(15000, position.total_buy_price)
        self.assertEqual(100, position.current_share_price)
        self.assertEqual(75, position.average_buy_price)
        self.assertEqual(-5000, position.p_and_l)
        self.assertEqual(25000, position.realized_p_and_l)
        self.assertEqual(10000, position.position_size)

        self.assertEqual(20000, self.wallet.balance)
        self.assertEqual(25000, self.wallet.equity)
        self.assertEqual(70000, self.wallet.buying_power)

        self.manager.cover_shares(self.wallet,
                                  ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                             open=150, high=50, low=50, close=50, adj_close=50, volume=10000), 200,
                                  datetime.now, position)

        self.assertEqual(0, position.current_amount)
        self.assertEqual(0, position.total_buy_price)
        self.assertEqual(150, position.current_share_price)
        self.assertEqual(0, position.average_buy_price)
        self.assertEqual(0, position.p_and_l)
        self.assertEqual(10000, position.realized_p_and_l)
        self.assertEqual(0, position.position_size)

        self.assertEqual(10000, self.wallet.balance)
        self.assertEqual(10000, self.wallet.equity)
        self.assertEqual(40000, self.wallet.buying_power)

    def test_stop_loss_long(self):
        position: Position = self.wallet.positions[-1]

        self.manager.buy_shares(self.wallet,
                                ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                           open=50, high=50, low=50, close=50, adj_close=50, volume=10000), 100,
                                datetime(2019, 1, 1), position)

        position.add_stop_loss(datetime(2019, 1, 1), 40)

        self.assertFalse(position.hit_stop_loss(datetime(2019, 1, 1), 41, 50))

        position.add_stop_loss(datetime(2019, 1, 2), 40)

        self.assertTrue(position.hit_stop_loss(datetime(2019, 1, 2), 39, 50))
        self.assertTrue(position.hit_stop_loss(datetime(2019, 1, 2), 40, 50))

    def test_stop_loss_short(self):
        position: Position = self.wallet.positions[-1]

        self.manager.short_shares(self.wallet,
                                  ShareEntry(name="TEST", date=datetime.now, freq=str(Frequency.ONE_DAY),
                                             open=50, high=50, low=50, close=50, adj_close=50, volume=10000), 100,
                                  datetime(2019, 1, 1), position)

        position.add_stop_loss(datetime(2019, 1, 1), 40)

        self.assertFalse(position.hit_stop_loss(datetime(2019, 1, 1), 35, 38))

        position.add_stop_loss(datetime(2019, 1, 2), 40)

        self.assertTrue(position.hit_stop_loss(datetime(2019, 1, 2), 35, 41))
        self.assertTrue(position.hit_stop_loss(datetime(2019, 1, 2), 35, 40))
