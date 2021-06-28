from abc import ABC, abstractmethod

from ai.agent.episode import Episode
from ai.agent.percept import Percept
from ai.enviroment.environment import Environment
from properties.properties import Properties


class LearningStrategy(ABC):
    """
    Implementations of this class represent a Learning Method
    Deze klasse is ONVOLLEDIG
    """
    env: Environment
    properties: Properties = Properties()

    def __init__(self, environment: Environment, λ, γ, t_max) -> None:
        self.env = environment
        self.λ = λ  # exponential decay rate used for exploration/exploitation (given)
        self.γ = γ  # discount rate for exploration (given)
        self.ε_max = self.properties.ls_ε_max  # Exploration probability at start (given)
        self.ε_min = self.properties.ls_ε_min  # Minimum exploration probability (given)

        self.ε = self.ε_max  # (decaying) probability of selecting random action according to ε-soft policy
        self.t_max = t_max  # upper limit voor episode
        self.t = 0  # episode time step
        self.τ = 0  # overall time step

    @abstractmethod
    def next_action(self, state):
        pass

    @abstractmethod
    def learn(self, episode: Episode, **kwargs):
        # implementatie uit subklassen komt voor deze statements:
        self.t += 1
        if episode.size > 0:
            p: Percept = episode.percepts(-1)
            if p.done:
                self.τ += 1

    @abstractmethod
    def start_episode(self):
        self.t = 0

    def decay(self):
        pass

    def done(self):
        return self.t > self.t_max and self.properties.ls_use_t_max
