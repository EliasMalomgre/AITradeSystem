import numpy as np

from ai.agent.agent import Agent
from ai.agent.episode import Episode
from ai.agent.percept import Percept
from ai.enviroment.environment import Environment
from ai.learning.policy_gradient.a2c import A2C
from ai.learning.policy_gradient.gradient_duplicate_layers import GradientDuplicateLayers
from domain.action import Action
from plots.epsiode_reward_plot import EpisodeRewards
from properties.properties import Properties
from properties.simulation_type import SimulationType


class GradientAgent(Agent):
    properties: Properties = Properties()

    def __init__(self, environment: Environment, learning_strategy: GradientDuplicateLayers,
                 n_episodes=properties.agent_max_episodes):
        super().__init__(environment, n_episodes=n_episodes)
        self.learning_strategy = learning_strategy

    def train(self) -> None:
        state_dim = self.learning_strategy.state_dim
        rewards = 0
        episode_rewards: [float] = []
        total_percepts = 0

        while not self.done:
            self.properties.agent_save_training_sessions = False

            if self.episode_count % self.properties.agent_save_after_n_episodes == 0:
                self.properties.agent_save_training_sessions = True

            # start a new episode
            episode = Episode(self.env)
            self.episodes.append(episode)
            # initialize the start state
            state = self.env.reset()

            # reset the learning strategy
            self.learning_strategy.start_episode()

            episode_rewards.append(0)
            percept_count = 1

            # while the episode isn't finished by length
            while not self.learning_strategy.done():
                # Get outputs from policy gradient network
                outputs = self.learning_strategy.next_action(state)

                # Depending on which actions are allowed create
                if self.properties.simulator_simulation_type == SimulationType.ALL_ACTIONS:
                    action = Action(stop_loss=outputs[0][0], buy=round(outputs[0][1]),
                                    sell=round(outputs[0][2]), short=round(outputs[0][3]), cover=round(outputs[0][4]))
                elif self.properties.simulator_simulation_type == SimulationType.ONLY_BUY_AND_SELL:
                    action = Action(stop_loss=outputs[0][0][0], buy=round(outputs[1][0][0]),
                                    sell=round(outputs[2][0][0]))
                elif self.properties.simulator_simulation_type == SimulationType.ONLY_BUY_AND_SELL:
                    action = Action(stop_loss=outputs[0][0], short=round(outputs[0][1]),
                                    cover=round(outputs[0][2]))
                else:
                    action = Action(buy=outputs[0][0][0], sell=round(outputs[1][0][0]))

                # Make step
                observation = self.env.step(action, state)

                # create Percept from s,a,r,s' and add to Episode
                percept: Percept = Percept((state, outputs) + observation)

                episode.add(percept)

                # Add reward to the episode rewards
                episode_rewards[-1] += percept.reward

                state = percept.next_state

                # Reshape percept states
                percept.next_state = np.reshape(percept.next_state.to_array(), [1, state_dim])
                percept.state = np.reshape(percept.state.to_array(), [1, state_dim])

                # Print percept info when configured
                if self.properties.agent_show_percept_rewards:
                    print("Percept count: {} Percept reward {}".format(percept_count, percept.reward))
                percept_count += 1

                # Learn and if learning strategy is A2C learn, calculate v
                if isinstance(self.learning_strategy, A2C):
                    v = 0 if percept.reward > 0 else \
                        self.learning_strategy.value(np.reshape(state.to_array(), [1, state_dim]))[0]
                    self.learning_strategy.learn(episode, last_value=v)
                else:
                    self.learning_strategy.learn(episode)

                if percept.done:
                    break

            # Print episode info when configured
            if self.properties.agent_show_episode_rewards:
                print("Episode count: {} Rewards: {}\n".format(self.episode_count, episode_rewards[-1]))

            rewards += episode_rewards[-1]
            total_percepts += percept_count

            # Show detailed summary
            if self.properties.agent_show_summary and \
                    self.episode_count % self.properties.agent_reward_summary_n_episodes == 0:
                print("\n============================================================")
                print("Episode {}".format(self.episode_count))
                print("Total reward {}".format(rewards))
                print("Average reward {}".format(rewards / self.properties.agent_reward_summary_n_episodes))
                print("Average percepts {}".format(total_percepts / self.properties.agent_reward_summary_n_episodes))
                print("============================================================\n")
                rewards = 0
                total_percepts = 0

            # Plot reward history
            if self.episode_count % self.properties.agent_reward_plot_n_episodes == 0:
                EpisodeRewards().plot(episode_rewards)

            # Save model weights
            if self.properties.gradient_save_weights and \
                    self.episode_count % self.properties.gradient_save_weight_n_episodes == 0:
                self.learning_strategy.save_weights(self.properties.gradient_actor_model_weights,
                                                    self.properties.gradient_value_model_weights)
            self.episode_count += 1
            self.env.close()
