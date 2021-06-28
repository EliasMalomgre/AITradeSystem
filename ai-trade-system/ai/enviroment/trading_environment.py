import random
from abc import ABC
from datetime import datetime
from math import floor

from ai.enviroment.environment import Environment
from application.stock_simulator import StockSimulator
from domain.action import Action
from domain.bar import Bar
from domain.frequency import Frequency
from domain.share_entry import ShareEntry
from domain.state import State
from properties.properties import Properties


class TradingSystem(Environment, ABC):
    properties: Properties = Properties()

    def __init__(self, stock_name: str = properties.default_stock_name, frequency: Frequency = properties.default_freq,
                 start_date: datetime = properties.simulator_simulation_data_start,
                 end_date: datetime = properties.simulator_simulation_data_end,
                 custom_start_date: datetime = properties.simulator_custom_start_date):
        self.properties = Properties()
        self.simulator = StockSimulator(stock_name=stock_name, frequency=frequency, start_date=start_date,
                                        end_date=end_date, custom_start_date=custom_start_date)

    def reset(self) -> State:
        return self.simulator.reset_simulation()

    def step(self, action: Action, state: State) -> (State, float, bool):
        return self.simulator.next_action(action, state)

    def render(self):
        pass

    def close(self) -> None:
        self.simulator.close_simulation()

    @property
    def state_size(self):
        return self.properties.bar_attribute_count * self.properties.state_bar_count + \
               self.properties.state_attribute_count

    @property
    def action_space(self):
        return None

    @property
    def observation_space(self):
        return None

    @property
    def n_actions(self):
        return self.properties.gradient_default_output_count

    @property
    def isdiscrete(self) -> bool:
        return False

    @property
    def name(self) -> str:
        return "Stonksbot"

    def sample(self):
        """Samples random State"""
        # Get random data out of the simulation data
        data: [ShareEntry] = self.simulator.simulation_data
        random.shuffle(data)
        data = data[-self.properties.state_bar_count:]

        bars = []
        random_value = 0.0
        # Create random bars out of the simulation data
        for entry in data:
            random_value = random.random()
            bars.append(Bar(entry.date, entry.open, entry.high, entry.low, entry.close, entry.adj_close, entry.volume,
                            round(random_value * 200), (random_value * (self.properties.simulator_max_stop_loss_value -
                                                                        self.properties.simulator_min_stop_loss_value))
                            + self.properties.simulator_min_stop_loss_value))
        # Parse data to a State
        return State(random_value * 50000, floor(random_value * 3),
                     bars)
