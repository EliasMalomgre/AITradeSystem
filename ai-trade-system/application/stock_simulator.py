import datetime

from application.bank_manager import BankManager
from application.static_declarations import create_position
from domain.action import Action
from domain.bar import Bar
from domain.frequency import Frequency
from domain.position import Position
from domain.position_status import PositionStatus
from domain.share_entry import ShareEntry
from domain.state import State
from domain.wallet import Wallet
from properties.properties import Properties
from properties.simulation_type import SimulationType
from repositories.stock_repository import StockRepository
from repositories.transaction_repository import TransactionRepository


class StockSimulator:
    properties: Properties = Properties()

    def __init__(self, stock_name: str = properties.default_stock_name, frequency: Frequency = properties.default_freq,
                 start_date: datetime = properties.simulator_simulation_data_start,
                 end_date: datetime = properties.simulator_simulation_data_end,
                 custom_start_date: datetime = properties.simulator_custom_start_date):

        self.stock_name = stock_name
        self.frequency = frequency
        self.start_date = start_date
        self.end_date = end_date
        self.custom_start_date = custom_start_date
        self.stock_repository: StockRepository = StockRepository()
        self.transaction_repository: TransactionRepository = TransactionRepository()
        self.bank_manager: BankManager = BankManager()
        self.wallet: Wallet = TransactionRepository().get_wallet()
        self.simulation_data: [ShareEntry] = []
        # Load simulation data
        self.get_simulation_data(self.start_date, self.end_date, self.stock_name, self.frequency)
        self.is_setup_phase = True

    def get_simulation_data(self, start_date: datetime, end_date, stock_name: str, freq: Frequency):
        """Pulls all the necessary data for the simulation"""
        self.simulation_data = []

        for entry in self.stock_repository.get_entries_between(stock_name, start_date, end_date, freq):
            self.simulation_data.append(entry)

    def get_stock_data(self, start_date=None):
        """Gets the data for date. If not found get next time frame"""

        # Get index for date
        index = self.get_simulation_index(start_date)
        # Get the default fail safe value
        fail_safe = self.properties.simulator_get_stock_data_fail_safe
        # While there is no index found for the date
        while index is None:
            # Switch over time frames and add 1 time frame
            if self.frequency == Frequency.ONE_MINUTE:
                start_date += datetime.timedelta(minutes=1)
            elif self.frequency == Frequency.ONE_HOUR:
                start_date += datetime.timedelta(hours=1)
            elif self.frequency == Frequency.ONE_DAY:
                start_date += datetime.timedelta(days=1)
            elif self.frequency == Frequency.ONE_WEEK:
                start_date += datetime.timedelta(weeks=1)
            elif self.frequency == Frequency.ONE_MONTH:
                pass
            # Try to get index for the date
            index = self.get_simulation_index(start_date)
            fail_safe -= 1
            # If fail safe is hit throw exception
            if fail_safe < 0:
                raise Exception("StockSimulator infinite loop get stock data")

        return self.simulation_data[index - (self.properties.state_bar_count - 1): index + 1]

    def next_action(self, action: Action, state: State):
        """Processed incoming action and returns reward and next state"""

        # Get current and previous bar
        previous_bar: Bar = state.bars[-1]
        current_bar: Bar = self.simulation_data[self.get_simulation_index(previous_bar.date) + 1]

        # Get balance before action to calculate reward
        balance_before = self.wallet.balance

        # Update the current posiition
        position: Position = self.get_position()
        position.current_share_price = current_bar.open
        position.update_p_and_l()
        self.wallet.update_equity()

        # Proces stop loss
        self.check_stop_loss_hit(position, current_bar, previous_bar)
        stop_loss = self.calculate_stop_loss(action, current_bar, previous_bar, position)

        # Rectify mistakes if configured
        if self.properties.simulator_ignore_mistakes:
            self.ignore_illegal_actions(position, action)

        # Check for illegal actions and punish if needed
        if self.check_illegal_actions(action, position, stop_loss, current_bar, previous_bar):
            return self.get_state(current_bar.date), -1, True

        # Execute a transaction if needed
        if action.buy == 1 or action.sell == 1 or action.short == 1 or action.cover == 1:
            self.execute_transaction(action, self.wallet, position, current_bar.date, stop_loss, current_bar.open)

        # Add the new stop loss to the posiiton if postion amount is not 0
        if position.current_amount != 0:
            position.add_stop_loss(current_bar.date, stop_loss)

        return self.get_state(current_bar.date), self.calculate_reward(balance_before), len(self.simulation_data) <= \
               self.get_simulation_index(current_bar.date) + 2

    def execute_transaction(self, action: Action, wallet: Wallet, position: Position, date: datetime, stop_loss, open):
        """Executes a transaction with the action of the ai"""

        # Switch over all transaction types
        if action.sell == 1:
            self.bank_manager.sell_shares(self.wallet, next(filter(lambda x: x.date == date, self.simulation_data)),
                                          position.current_amount, date, position)
        elif action.buy == 1:
            # Calculate amount
            amount = (position.risk * self.wallet.equity) / (open - stop_loss)

            # When ignoring mistakes make sure buying power doesn't goes negative
            if self.properties.simulator_ignore_mistakes:

                max_amount = wallet.buying_power / open

                if amount > max_amount:
                    amount = max_amount

            self.bank_manager.buy_shares(self.wallet, next(filter(lambda x: x.date == date, self.simulation_data)),
                                         amount, date, position)
        elif action.short == 1:
            # Calculate amount
            amount = (position.risk * self.wallet.equity) / (open - stop_loss)

            # When ignoring mistakes make sure buying power doesn't goes negative
            if self.properties.simulator_ignore_mistakes:
                max_amount = wallet.buying_power / open

                if amount > max_amount:
                    amount = max_amount

            self.bank_manager.short_shares(self.wallet, next(filter(lambda x: x.date == date, self.simulation_data)),
                                           amount, date, position)
        elif action.cover == 1:
            self.bank_manager.cover_shares(self.wallet, next(filter(lambda x: x.date == date, self.simulation_data)),
                                           -position.current_amount, date, position)

    def reset_simulation(self) -> State:
        """Resets the simulator"""
        self.close_simulation()

        # Use custom start date if configured
        if self.properties.simulator_use_custom_start_date:
            start_date = self.custom_start_date
        else:
            start_date = self.simulation_data[self.properties.state_bar_count - 1].date

        # Reset wallet
        self.wallet.equity = self.properties.simulator_reset_wallet_equity
        self.wallet.update_equity()

        # Create postion and save when configured
        position: Position = create_position(self.stock_name, self.frequency.value)
        if self.properties.agent_save_training_sessions:
            self.transaction_repository.save_position(position)

        # Add postion and save when configured
        self.wallet.positions.append(position)
        if self.properties.agent_save_training_sessions:
            self.transaction_repository.save_wallet(self.wallet)

        return self.get_state(start_date)

    def get_state(self, date: datetime) -> State:
        """Creates a State with incoming date"""
        position: Position = self.get_position()
        # Get all simulation data
        entries: [] = self.get_stock_data(date)

        # Parse simulation data to a State
        state: State = State(self.wallet.buying_power, position.get_status().value,
                             list(map(lambda x: Bar(x.date, x.open, x.high, x.low, x.close, x.adj_close, x.volume,
                                                    position.current_amount, position.get_stop_loss(x.date)), entries)))

        return state

    def close_simulation(self):
        """Executes logic to stop a simulation"""
        # Closes all positions and saves when configured
        for position in filter(lambda x: x.open, self.wallet.positions):
            position.open = False
            if self.properties.agent_save_training_sessions and len(list(filter(lambda x: x.id is None,
                                                                                position.current_transactions))) == 0:
                self.transaction_repository.save_position(position)

    def get_position(self):
        """Gets the latest open position"""
        return next(filter(lambda x: x.open, self.wallet.positions))

    def calculate_reward(self, balance_before):
        """Calculates the reward for a percept"""
        # Calculate the percentage of the balance won or lost
        return (self.wallet.balance / balance_before) - 1

    def check_illegal_actions(self, action: Action, position: Position, stop_loss, current_bar: Bar, previous_bar: Bar):
        """Checks for illegal moves"""

        position_status = position.get_status()

        # Check if action is possible
        if action.buy == 1 and position.current_amount < 0:
            return True
        elif action.short == 1 and position.current_amount > 0:
            return True
        elif action.cover == 1 and position.current_amount >= 0:
            return True
        elif action.sell == 1 and position.current_amount <= 0:
            return True
        # Check if stop loss is correct
        elif position_status == PositionStatus.LONG and stop_loss >= current_bar.open:
            return True
        elif position_status == PositionStatus.SHORT and stop_loss <= current_bar.open:
            return True
        elif position_status == PositionStatus.NONE and action.buy == 1 and stop_loss >= current_bar.open:
            return True
        elif position_status == PositionStatus.NONE and action.short == 1 and stop_loss <= current_bar.open:
            return True
        elif self.properties.simulator_prevent_wrong_stop_loss_change and previous_bar.current_amount > 0 and \
                stop_loss < previous_bar.stop_loss and position.current_amount > 0:
            return True
        elif self.properties.simulator_prevent_wrong_stop_loss_change and previous_bar.current_amount < 0 and \
                stop_loss > previous_bar.stop_loss and position.current_amount < 0:
            return True
        # Check for multiple action
        elif [action.buy, action.sell, action.short, action.cover].count(1.0) > 1:
            return True
        # Check wallet data
        elif self.wallet.equity < 0:
            return True
        elif self.wallet.balance < 0:
            return True
        elif self.wallet.buying_power < 0:
            return True

        return False

    @staticmethod
    def ignore_illegal_actions(position: Position, action: Action):
        """Corrects actions that are not possible"""
        if action.buy == 1 and position.current_amount < 0:
            action.buy = 0
        elif action.short == 1 and position.current_amount > 0:
            action.short = 0
        elif action.cover == 1 and position.current_amount >= 0:
            action.cover = 0
        elif action.sell == 1 and position.current_amount <= 0:
            action.sell = 0
        elif [action.buy, action.sell, action.short, action.cover].count(1.0) > 1:
            action.buy = 0
            action.sell = 0
            action.short = 0
            action.cover = 0

    def get_simulation_index(self, date: datetime):
        """Tries to return index else returns None"""
        try:
            return list(map(lambda x: x.date, self.simulation_data)).index(date)
        except:
            return None

    def calculate_stop_loss(self, action: Action, current_bar: Bar, previous_bar: Bar, position: Position):
        """Calculates stop loss for incoming action"""
        # If all actions are allowed in the simulation
        if self.properties.simulator_simulation_type == SimulationType.ALL_ACTIONS:
            return (action.stop_loss * self.properties.simulator_max_stop_loss_value -
                    self.properties.simulator_min_stop_loss_value) + self.properties.simulator_min_stop_loss_value

        # If only buy and sell are allowed in the simulation
        elif self.properties.simulator_simulation_type == SimulationType.ONLY_BUY_AND_SELL:
            # If you don't ignore mistakes calculate normally
            if not self.properties.simulator_ignore_mistakes:
                return action.stop_loss * current_bar.open
            else:
                # Calculate stop loss
                if not self.properties.simulator_ignore_mistakes or action.stop_loss != 1:
                    stop_loss = action.stop_loss * current_bar.open
                else:
                    stop_loss = self.properties.simulator_buy_sell_max_stop_loss * current_bar.open

                # If you want to prevent wrong stop loss changes and the previous bar had shares
                if self.properties.simulator_prevent_wrong_stop_loss_change and previous_bar.current_amount > 0 \
                        and position.current_amount > 0:
                    # If new stop loss is lower than the previous one
                    if stop_loss < previous_bar.stop_loss:
                        # Set the new value to the old one
                        stop_loss = previous_bar.stop_loss

                return stop_loss
        # If only short and cover are allowed in the simulation
        elif self.properties.simulator_simulation_type == SimulationType.ONLY_SHORT_COVER:
            if not self.properties.simulator_ignore_mistakes:
                return current_bar.open + action.stop_loss * (
                        self.properties.simulator_max_stop_loss_value - current_bar.open)
            else:
                # Calculate stop loss
                if not self.properties.simulator_ignore_mistakes or action.stop_loss != 0:
                    stop_loss = current_bar.open + action.stop_loss * (
                            self.properties.simulator_max_stop_loss_value - current_bar.open)
                else:
                    stop_loss = current_bar.open + self.properties.simulator_short_cover_min_stop_loss * (
                            self.properties.simulator_max_stop_loss_value - current_bar.open)

                if self.properties.simulator_prevent_wrong_stop_loss_change and previous_bar.current_amount > 0 \
                        and position.current_amount < 0:
                    # If new stop loss is lower than the previous one
                    if stop_loss > previous_bar.stop_loss:
                        # Set the new value to the old one
                        stop_loss = previous_bar.stop_loss

                return stop_loss

        else:
            stop_loss = self.properties.simulator_buy_sell_no_sl_value * current_bar.open

            if self.properties.simulator_prevent_wrong_stop_loss_change and previous_bar.current_amount > 0 \
                    and position.current_amount > 0:
                # If new stop loss is lower than the previous one
                if stop_loss < previous_bar.stop_loss:
                    # Set the new value to the old one
                    stop_loss = previous_bar.stop_loss

            return stop_loss

    def check_stop_loss_hit(self, position: Position, current_bar: Bar, previous_bar: Bar):
        """Checks for stop loss hits and sells/cover when hit occurs"""
        # Check if stop loss has been hit
        if position.hit_stop_loss(previous_bar.date, current_bar.low, current_bar.high):
            # If in long position
            if position.get_status() == PositionStatus.LONG:
                # Sell all shares
                self.bank_manager.sell_shares(self.wallet, next(filter(lambda x: x.date == current_bar.date,
                                                                       self.simulation_data)),
                                              position.current_amount,
                                              current_bar.date, position, previous_bar.stop_loss)
            # If in short position
            else:
                # Cover all shares
                self.bank_manager.cover_shares(self.wallet, next(filter(lambda x: x.date == current_bar.date,
                                                                        self.simulation_data)),
                                               position.current_amount * -1,
                                               current_bar.date, position, previous_bar.stop_loss)
