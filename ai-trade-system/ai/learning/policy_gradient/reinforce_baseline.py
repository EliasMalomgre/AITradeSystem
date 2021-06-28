import numpy as np

from ai.agent.episode import Episode
from ai.agent.percept import Percept
from ai.enviroment.environment import Environment
from ai.learning.policy_gradient.reinforce import Reinforce
from properties.properties import Properties


class ReinforceBaseLine(Reinforce):
    properties: Properties = Properties()

    def __init__(self, environment: Environment, λ=properties.base_rein_λ, γ=properties.base_rein_γ,
                 t_max=properties.base_rein_t_max):
        super().__init__(environment, λ, γ, t_max)

    def next_action(self, state):
        return super().next_action(state)

    def learn(self, episode: Episode, **kwargs):
        super().learn(episode)

    def start_episode(self):
        super().start_episode()

    def train(self, percept: Percept, step: int, gamma=properties.base_rein_default_gamma):
        """Main routine for training
        Arguments:
            item (list) : one experience unit
            gamma (float) : discount factor [0,1]
        """
        # must save state for entropy computation
        self.state = percept.state

        discount_factor = gamma ** step

        # reinforce-baseline: delta = return - value
        delta = percept.reward - self.value(self.state)[0]

        # apply the discount factor as shown in Algorithms
        # 10.2.1, 10.3.1 and 10.4.1
        discounted_delta = delta * discount_factor
        discounted_delta = np.reshape(discounted_delta, [-1, 1])
        verbose = self.properties.base_rein_done_verbose if percept.done else self.properties.base_rein_default_verbose

        # train the logp model (implies training of actor model
        # as well) since they share exactly the same set of
        # parameters
        self.logp_model.fit(np.array(self.state),
                            discounted_delta,
                            batch_size=1,
                            epochs=self.properties.base_rein_logp_epochs,
                            verbose=verbose)

        # train the value network (critic)
        self.value_model.fit(np.array(self.state),
                             discounted_delta,
                             batch_size=1,
                             epochs=self.properties.base_rein_value_epochs,
                             verbose=verbose)
