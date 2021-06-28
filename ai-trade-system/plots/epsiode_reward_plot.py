from functools import reduce

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.figure import Figure

from properties.properties import Properties


class EpisodeRewards:
    def __init__(self):
        self.properties = Properties()

    def plot(self, episode_rewards):

        figure: Figure
        with plt.rc_context(dict(
                sns.axes_style("whitegrid"),
                **sns.plotting_context("paper", font_scale=1, rc={"grid.linewidth": .35})
        )):
            figure, ax = plt.subplots()
            figure.suptitle("Average rewards of n episodes", fontsize=20)
            ax.set_xlabel("Episodes", size=14)
            ax.set_ylabel("Rewards", size=14)
            ax.tick_params(axis='both', labelsize=12)

            for mean_of_n_episodes in self.properties.plot_reward_plot_means:
                mean_rewards = []
                for array in [episode_rewards[i * mean_of_n_episodes:(i + 1) * mean_of_n_episodes] for i in
                              range((len(episode_rewards) + mean_of_n_episodes - 1) // mean_of_n_episodes)]:
                    mean_rewards.append(reduce(lambda x, y: x + y, array) / len(array))
                ax.plot(np.arange(0, len(mean_rewards), 1) * mean_of_n_episodes, mean_rewards,
                        label='ma' + str(mean_of_n_episodes))

            ax.legend(loc='upper center', ncol=3, frameon=False, fontsize=10)

        if self.properties.plot_reward_plot_show:
            plt.show()

        if self.properties.plot_reward_plot_save:
            figure.savefig(self.properties.plot_image_folder + self.properties.plot_reward_plot_name +
                           self.properties.plot_default_image_type)
