import math
from abc import ABC

import numpy as np

from ai.agent.episode import Episode
from ai.agent.percept import Percept
from ai.enviroment.environment import Environment
from ai.learning.policy_gradient.gradient_multiple_outputs import GradientMultipleOutputs
from properties.properties import Properties


class Reinforce(GradientMultipleOutputs, ABC):
    properties: Properties = Properties()

    def __init__(self, environment: Environment, λ=properties.rein_λ, γ=properties.rein_γ,
                 t_max=properties.rein_t_max):
        super().__init__(environment, λ, γ, t_max)

    def next_action(self, state):
        return super().next_action(state)

    def learn(self, episode: Episode, **kwargs):
        super().learn(episode)
        p: Percept = episode.percepts(-1)
        if p.done:
            self.train_by_episode(episode)

    def start_episode(self):
        super().start_episode()

    def train_by_episode(self, episode: Episode):
        """Train by episode
           Prepare the dataset before the step by step training
        """
        # only REINFORCE and REINFORCE with baseline
        # use the ff code
        # convert the rewards to returns
        rewards = []
        gamma = self.properties.rein_gamma
        for percept in episode.get_percepts():
            rewards.append(percept.reward)
        # rewards = np.array(self.memory)[:,3].tolist()

        # compute return per step
        # return is the sum of rewards from t til end of episode
        # return replaces reward in the list
        for i in range(len(rewards)):
            reward = rewards[i:]
            horizon = len(reward)
            discount = [math.pow(gamma, t) for t in range(horizon)]
            return_ = np.dot(reward, discount)
            episode.percepts(i).reward = return_

        # train every step
        for step, percept in zip(range(len(episode.get_percepts()), -1, -1), episode.get_percepts()):
            self.train(percept, step, gamma=gamma)

    def train(self, percept: Percept, step: int, gamma=properties.rein_default_gamma):
        """Main routine for training
        Arguments:
            item (list) : one experience unit
            gamma (float) : discount factor [0,1]
        """
        # must save state for entropy computation
        self.state = percept.state

        discount_factor = gamma ** step
        delta = percept.reward

        # apply the discount factor as shown in Algortihms
        # 10.2.1, 10.3.1 and 10.4.1
        discounted_delta = delta * discount_factor
        discounted_delta = np.reshape(discounted_delta, [-1, 1])
        verbose = self.properties.rein_done_verbose if percept.done else self.properties.rein_default_verbose

        # train the logp model (implies training of actor model
        # as well) since they share exactly the same set of
        # parameters
        self.logp_model.fit(np.array(self.state),
                            discounted_delta,
                            batch_size=1,
                            epochs=self.properties.rein_logp_epochs,
                            verbose=verbose)
