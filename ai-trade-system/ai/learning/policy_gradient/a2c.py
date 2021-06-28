from abc import ABC

import numpy as np

from ai.agent.episode import Episode
from ai.agent.percept import Percept
from ai.enviroment.environment import Environment
from ai.learning.policy_gradient.gradient_duplicate_layers import GradientDuplicateLayers
from properties.properties import Properties


class A2C(GradientDuplicateLayers, ABC):
    properties: Properties = Properties()

    def __init__(self, environment: Environment, λ=properties.a2c_λ, γ=properties.a2c_γ,
                 t_max=properties.a2c_t_max):
        super().__init__(environment, λ, γ, t_max)

    def next_action(self, state):
        return super().next_action(state)

    def learn(self, episode: Episode, **kwargs):
        super().learn(episode)
        p: Percept = episode.percepts(-1)
        if p.done or self.done():
            self.train_by_episode(episode)

    def start_episode(self):
        super().start_episode()

    def train_by_episode(self, episode: Episode, last_value=0):
        """Train by episode
           Prepare the dataset before the step by step training
        Arguments:
            last_value (float): previous prediction of value net
        """
        # implements A2C training from the last state
        # to the first state
        # discount factor
        gamma = self.properties.a2c_gamma
        r = last_value
        # the memory is visited in reverse as shown
        # in Algorithm 10.5.1
        for step, percept in zip(range(len(episode.get_percepts()), -1, -1), reversed(episode.get_percepts())):
            # compute the return
            percept.reward = percept.reward + gamma * r
            # train per step
            # a2c reward has been discounted
            self.train(percept, step)

    def train(self, percept: Percept, step: int, gamma=properties.a2c_default_gamma):

        # must save state for entropy computation
        self.state = percept.state

        discount_factor = gamma ** step

        # a2c: delta = discounted_reward - value
        delta = percept.reward - self.value(self.state)[0]

        discounted_delta = delta * discount_factor
        discounted_delta = np.reshape(discounted_delta, [-1, 1])
        verbose = self.properties.a2c_done_verbose if percept.done else self.properties.a2c_default_verbose

        # train the logp model (implies training of actor model
        # as well) since they share exactly the same set of
        # parameters
        self.logp_model.fit(np.array(self.state),
                            discounted_delta,
                            batch_size=1,
                            epochs=self.properties.a2c_logp_epochs,
                            verbose=verbose)

        # in A2C, the target value is the return (reward
        # replaced by return in the train_by_episode function)
        discounted_delta = percept.reward
        discounted_delta = np.reshape(discounted_delta, [-1, 1])

        # train the value network (critic)
        self.value_model.fit(np.array(self.state),
                             discounted_delta,
                             batch_size=1,
                             epochs=self.properties.a2c_value_epochs,
                             verbose=verbose)
