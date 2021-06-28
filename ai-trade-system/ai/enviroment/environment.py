from abc import ABC, abstractmethod


class Environment(ABC):
    """Abstract Environment"""

    @abstractmethod
    def reset(self):
        # New random wallet
        pass

    @abstractmethod
    def step(self, action, state):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @property
    @abstractmethod
    def action_space(self):
        pass

    @property
    @abstractmethod
    def observation_space(self):
        pass

    @property
    @abstractmethod
    def n_actions(self):
        pass

    @property
    @abstractmethod
    def state_size(self):
        pass

    @property
    @abstractmethod
    def isdiscrete(self) -> bool:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def sample(self):
        pass
