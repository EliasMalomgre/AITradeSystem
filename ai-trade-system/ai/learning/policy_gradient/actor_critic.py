from abc import ABC

import numpy as np

from ai.agent.episode import Episode
from ai.agent.percept import Percept
from ai.enviroment.environment import Environment
from ai.learning.policy_gradient.gradient_duplicate_layers import GradientDuplicateLayers
from properties.properties import Properties


class ActorCritic(GradientDuplicateLayers, ABC):
    properties: Properties = Properties()

    def __init__(self, environment: Environment, λ=properties.ac_λ, γ=properties.ac_γ,
                 t_max=properties.ac_t_max):
        super().__init__(environment, λ, γ, t_max)

    def next_action(self, state):
        return super().next_action(state)

    def learn(self, episode: Episode, **kwargs):
        super().learn(episode, **kwargs)
        self.train(episode.percepts(-1), len(episode.get_percepts()), gamma=self.properties.ac_gamma)

    def start_episode(self):
        super().start_episode()

    def train(self, percept: Percept, step: int, gamma=properties.ac_default_gamma):
        # must save state for entropy computation
        self.state = percept.state

        discount_factor = gamma ** step

        # actor-critic: delta = reward - value
        #       + discounted_next_value
        delta = percept.reward - self.value(self.state)[0]

        # since this function is called by Actor-Critic
        # directly, evaluate the value function here
        if not percept.done:
            next_value = self.value(self.state)[0]
            # add  the discounted next value
            delta += gamma * next_value

        # apply the discount factor as shown in Algorithms
        # 10.2.1, 10.3.1 and 10.4.1
        discounted_delta = delta * discount_factor
        discounted_delta = np.reshape(discounted_delta, [-1, 1])
        verbose = self.properties.ac_done_verbose if percept.done else self.properties.ac_default_verbose

        # train the logp model (implies training of actor model
        # as well) since they share exactly the same set of
        # parameters
        self.logp_model.fit(np.array(self.state),
                            discounted_delta,
                            batch_size=1,
                            epochs=self.properties.ac_logp_epochs,
                            verbose=verbose)

        self.value_model.fit(np.array(self.state),
                             discounted_delta,
                             batch_size=1,
                             epochs=self.properties.ac_value_epochs,
                             verbose=verbose)
