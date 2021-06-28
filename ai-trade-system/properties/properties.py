import logging
from datetime import datetime

from domain.frequency import Frequency
from domain.singleton import Singleton
from properties.simulation_type import SimulationType


class Properties(metaclass=Singleton):
    """This class is used to configure settings in the project"""

    def __init__(self):
        # Default stock
        self.default_stock_name: str = "AAPL"
        # Logging settings
        self.log_file: str = "logs/log1.log"
        self.log_level = logging.DEBUG

        # Db settings
        self.db_uri: str = \
            'mongodb+srv://admin:heelSecureWachtwoord@cluster0.y976o.mongodb.net/TradeDB?retryWrites=true&w=majority'

        # repo settings
        self.default_freq: Frequency = Frequency.ONE_DAY

        # Trading settings
        self.leverage = 4
        self.risk: float = 0.01
        self.wallet_equity: float = 25000

        # Learning strategy settings
        self.ls_ε_max = 1.0
        self.ls_ε_min = 0.0005
        self.ls_use_t_max = False

        # Gradient strategy settings
        self.gradient_λ = 0.00005
        self.gradient_γ = 0.95
        self.gradient_t_max = 17
        self.gradient_min_value = 0
        self.gradient_max_value = 1
        self.gradient_loss = 'mse'
        self.gradient_beta = 0.9
        self.gradient_lr = 1e-6
        self.gradient_default_output_count = 5
        self.gradient_save_weights = True
        self.gradient_save_weight_n_episodes = 500
        self.gradient_load_models = False
        self.gradient_model_folder = 'models/actor_value/'
        self.gradient_actor_model_weights = 'actor_weights'
        self.gradient_value_model_weights = 'value_weights'

        # Reinforced settings
        self.rein_λ = 0.00005
        self.rein_γ = 0.95
        self.rein_t_max = 17
        self.rein_gamma = 0.99
        self.rein_default_gamma = 1.0
        self.rein_default_verbose = 0
        self.rein_done_verbose = 0
        self.rein_logp_epochs = 1

        # Baseline Reinforced settings
        self.base_rein_λ = 0.00005
        self.base_rein_γ = 0.95
        self.base_rein_t_max = 17
        self.base_rein_default_gamma = 1.0
        self.base_rein_default_verbose = 0
        self.base_rein_done_verbose = 0
        self.base_rein_logp_epochs = 1
        self.base_rein_value_epochs = 1

        # Actor Critic settings
        self.ac_λ = 0.00005
        self.ac_γ = 0.95
        self.ac_t_max = 17
        self.ac_gamma = 0.99
        self.ac_default_gamma = 1.0
        self.ac_default_verbose = 0
        self.ac_done_verbose = 0
        self.ac_logp_epochs = 1
        self.ac_value_epochs = 1

        # A2C settings
        self.a2c_λ = 0.00005
        self.a2c_γ = 0.95
        self.a2c_t_max = 17
        self.a2c_gamma = 0.95
        self.a2c_default_gamma = 1.0
        self.a2c_default_verbose = 0
        self.a2c_done_verbose = 0
        self.a2c_logp_epochs = 1
        self.a2c_value_epochs = 1

        # Encoder settings
        self.encoder_batch_size = 128
        self.encoder_train_epochs = 2500
        self.encoder_sample_size = 200000
        self.encoder_feature_size = 64
        self.encoder_train_autoencoder = True
        self.encoder_save_autoencoder = True
        self.encoder_model_folder = 'models/encoder/'
        self.encoder_weights = 'encoder_weights'

        # Agent settings
        self.agent_save_training_sessions = False
        self.agent_show_percept_rewards = True
        self.agent_show_episode_rewards = True
        self.agent_show_summary = True
        self.agent_reward_summary_n_episodes = 1000
        self.agent_reward_plot_n_episodes = 500
        self.agent_max_episodes = 50000
        self.agent_episode_count = 1
        self.agent_save_after_n_episodes = 1000

        # State settings
        self.bar_attribute_count = 6
        self.state_attribute_count = 2
        self.state_bar_count = 30

        # StockSimulator settings
        self.simulator_simulation_data_start: datetime = datetime(2019, 1, 1)
        self.simulator_simulation_data_end: datetime = datetime(2019, 3, 1)
        self.simulator_use_custom_start_date: bool = True
        self.simulator_custom_start_date: datetime = datetime(2019, 2, 14)
        self.simulator_get_stock_data_fail_safe = 20
        self.simulator_reset_wallet_equity: float = 25000
        self.simulator_min_stop_loss_value: float = 0.0
        self.simulator_max_stop_loss_value: float = 250.0
        self.simulator_simulation_type: SimulationType = SimulationType.ONLY_BUY_AND_SELL
        self.simulator_ignore_mistakes = True
        self.simulator_buy_sell_max_stop_loss = 0.9999999999
        self.simulator_short_cover_min_stop_loss = 0.0000000001
        self.simulator_buy_sell_no_sl_value = 0.95
        self.simulator_prevent_wrong_stop_loss_change = True

        # Plot settings
        self.plot_image_folder = 'plot_images/'
        self.plot_default_image_type = '.png'
        self.plot_reward_plot_name = 'reward_plot'
        self.plot_reward_plot_means = [500, 1000, 5000]
        self.plot_reward_plot_show = True
        self.plot_reward_plot_save = False
