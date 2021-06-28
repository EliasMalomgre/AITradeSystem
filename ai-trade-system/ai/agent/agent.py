from abc import abstractmethod

from ai.agent.episode import Episode
from ai.enviroment.environment import Environment
from ai.learning.learningstrategy import LearningStrategy
from properties.properties import Properties


class Agent:
    properties: Properties = Properties()

    def __init__(self, environment: Environment, learning_strategy: LearningStrategy = LearningStrategy,
                 n_episodes=properties.agent_max_episodes):
        super().__init__()
        self.env = environment
        self.learning_strategy = learning_strategy
        self.episodes: [Episode] = []
        self.n_episodes = n_episodes  # total episodes
        self.episode_count = self.properties.agent_episode_count

    @abstractmethod
    def train(self) -> None:
        pass

    @property
    def done(self):
        return self.episode_count > self.n_episodes
