from abc import abstractmethod
from os import path, mkdir

import numpy as np
import tensorflow_probability as tfp
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.layers import Lambda, Activation
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import BatchNormalization
from tensorflow.python.keras.optimizer_v2.nadam import Nadam

from ai.agent.episode import Episode
from ai.agent.percept import Percept
from ai.enviroment.environment import Environment
from ai.learning.learningstrategy import LearningStrategy
from ai.learning.policy_gradient.encoder import AutoEncoder
from properties.properties import Properties
from properties.simulation_type import SimulationType


class GradientDuplicateLayers(LearningStrategy):
    properties: Properties = Properties()

    def __init__(self, environment: Environment, λ=properties.gradient_λ, γ=properties.gradient_γ,
                 t_max=properties.gradient_t_max, output_count=properties.gradient_default_output_count):
        super().__init__(environment, λ, γ, t_max)
        self.beta = self.properties.gradient_beta
        self.loss = self.properties.gradient_loss

        self.output_count = output_count
        if self.properties.simulator_simulation_type == SimulationType.ONLY_BUY_AND_SELL or \
                self.properties.simulator_simulation_type == SimulationType.ONLY_SHORT_COVER:
            self.output_count = 3
        elif self.properties.simulator_simulation_type == SimulationType.ONLY_BUY_AND_SELL_NO_SL:
            self.output_count = 2

        self.memory: [Percept] = []
        self.actor_models: [Model] = []
        self.state_dim = self.env.state_size
        self.state = self.env.reset().to_array()
        self.state = np.reshape(self.state, [1, self.state_dim])
        self.auto_encoder = AutoEncoder(self.state_dim, environment)

        if self.properties.encoder_train_autoencoder:
            self.auto_encoder.build_autoencoder()
            self.auto_encoder.train_autoencoder()
            self.auto_encoder.save_encoder_weights(self.properties.encoder_weights)
        else:
            self.auto_encoder.build_autoencoder()
            self.auto_encoder.load_encoder_weights(self.properties.encoder_weights)

        self.build_actor_critic()

    @abstractmethod
    def next_action(self, state):
        """
        Predicts an action for each actor model in the learning strategy

        :param state: The State for which action have to be predicted
        :return: The predicted actions of all the models
        """
        state = np.reshape(state.to_array(), [1, self.state_dim])
        actions: [] = []
        # Predict an action for all actor models in the learning strategy

        for model in self.actor_models:
            model: Model = model
            actions.append(model.predict(state)[0])
        return actions

    @abstractmethod
    def learn(self, episode: Episode, **kwargs):
        super().learn(episode, **kwargs)

    @abstractmethod
    def start_episode(self):
        super().start_episode()

    def action(self, args):
        """Given mean and stddev, sample an action, clip
            and return
            We assume Gaussian distribution of probability
            of selecting an action given a state
        Argument:
            args (list) : mean, stddev list
        Return:
            action (tensor): policy action
        """
        mean, stddev = args
        dist = tfp.distributions.Normal(loc=mean, scale=stddev)
        action = dist.sample(1)
        action = K.clip(action,
                        self.properties.gradient_min_value,
                        self.properties.gradient_max_value)
        return action

    def build_actor_critic(self):
        """4 models are built but 3 models share the
            same parameters. hence training one, trains the rest.
            The 3 models that share the same parameters
                are achtion, logp, and entropy models.
            Entropy model is used by A2C only.
            Each model as the same MLP structure:
            Input(2)-Encoder-Output(1).
            The output activation depends on the nature
                of the output.
        """
        inputs = Input(shape=(self.state_dim,), name='state')
        self.auto_encoder.encoder.trainable = False
        x = BatchNormalization()(inputs)
        x = self.auto_encoder.encoder(x)

        means, stddevs, actions = self.build_actor_models(inputs, x, self.output_count)

        logp = Lambda(self.logp,
                      output_shape=(1,),
                      name='logp')(means + stddevs + actions)
        self.logp_model = Model(inputs, logp, name='logp')
        self.logp_model.summary()

        entropy = Lambda(self.entropy,
                         output_shape=(1,),
                         name='entropy')(means + stddevs)
        self.entropy_model = Model(inputs, entropy, name='entropy')
        self.entropy_model.summary()

        value = Dense(1,
                      activation='linear',
                      kernel_initializer='zero',
                      name='value')(x)
        self.value_model = Model(inputs, value, name='value')
        self.value_model.summary()

        # logp loss of policy network
        loss = self.logp_loss(self.get_entropy(self.state),
                              beta=self.beta)
        optimizer = Nadam(lr=self.properties.gradient_lr)
        self.logp_model.compile(loss=loss, optimizer=optimizer)

        optimizer = Adam(lr=self.properties.gradient_lr)
        self.value_model.compile(loss=self.loss, optimizer=optimizer)

    def build_actor_models(self, inputs, x, outputs):
        """
        Creates a new mean, stddev and action layer for each output

        :param inputs: The inputs of the layer
        :param x: The layers before
        :param outputs: The amount of outputs of the network
        :return: A list of all the mean stddev and action layers
        """
        means: [] = []
        stddevs: [] = []
        actions: [] = []

        # Create a mean, stddev and action layer for each output
        for i in range(outputs):
            mean = Dense(1,
                         activation='linear',
                         kernel_initializer='zero',
                         name='mean' + str(i))(x)
            stddev = Dense(1,
                           kernel_initializer='zero',
                           name='stddev' + str(i))(x)
            # use of softplusk avoids stddev = 0
            stddev = Activation('softplusk', name='softplus' + str(i))(stddev)
            action = Lambda(self.action,
                            output_shape=(1,),
                            name='action' + str(i))([mean, stddev])
            # Add the action model the list of action models in the learning strategy
            self.actor_models.append(Model(inputs, action, name='action'))
            means.append(mean)
            stddevs.append(stddev)
            actions.append(action)
        return means, stddevs, actions

    @staticmethod
    def logp(args):
        """Given means, stddevs, and actions compute
            the log probability of the Gaussian distribution
        Argument:
            args (list) : means, stddevs, actions, list
        Return:
            logp (tensor): log of action
        """

        means, stddevs, actions = np.array_split(np.array(args), 3)
        dist = tfp.distributions.MultivariateNormalDiag(
            loc=means.tolist(), scale_diag=stddevs.tolist(),
            name='LogpMultivariateNormalDiag'
        )
        logp = dist.log_prob(actions.tolist())
        return logp

    @staticmethod
    def entropy(args):
        """Given the mean and stddev compute
            the Gaussian dist entropy
        Argument:
            args (list) : mean, stddev list
        Return:
            entropy (tensor): action entropy
        """
        means, stddevs = np.array_split(np.array(args), 2)
        dist = tfp.distributions.MultivariateNormalDiag(
            loc=means.tolist(), scale_diag=stddevs.tolist(),
            name='EntMultivariateNormalDiag')
        entropy = dist.entropy()
        return entropy

    def logp_loss(self, entropy, beta=0.0):
        """logp loss, the 3rd and 4th variables
            (entropy and beta) are needed by A2C
            so we have a different loss function structure
        Arguments:
            entropy (tensor): Entropy loss
            beta (float): Entropy loss weight
        Return:
            loss (tensor): computed loss
        """

        def loss(y_true, y_pred):
            test = -K.mean((y_pred * y_true) \
                           + (beta * entropy), axis=-1)
            return test

        return loss

    def value_loss(self, y_true, y_pred):
        """Typical loss function structure that accepts
            2 arguments only
           This will be used by value loss of all methods
            except A2C
        Arguments:
            y_true (tensor): value ground truth
            y_pred (tensor): value prediction
        Return:
            loss (tensor): computed loss
        """
        loss = -K.mean(y_pred * y_true, axis=-1)
        return loss

    def value(self, state):
        """Call the value network to predict the value of state
        Argument:
            state (tensor): environment state
        Return:
            value (tensor): state value
        """
        value = self.value_model.predict(state)
        return value[0]

    def get_entropy(self, state):
        """Return the entropy of the policy distribution
        Argument:
            state (tensor): environment state
        Return:
            entropy (tensor): entropy of policy
        """
        entropy = self.entropy_model.predict(state)
        return entropy[0]

    def save_weights(self,
                     actor_weights,
                     value_weights=None):
        """Save the actor, critic and encoder weights
            useful for restoring the trained models
        Arguments:
            actor_weights (tensor): actor net parameters
            encoder_weights (tensor): encoder weights
            value_weights (tensor): value net parameters
        """
        if not path.isdir(self.properties.encoder_model_folder):
            mkdir(self.properties.encoder_model_folder)

        for model, i in zip(self.actor_models, range(self.output_count)):
            model.save_weights(self.properties.gradient_model_folder + actor_weights + "_" + str(i) + ".h5")

        if value_weights is not None:
            self.value_model.save_weights(self.properties.gradient_model_folder + value_weights + ".h5")

    def load_weights(self,
                     actor_weights,
                     value_weights=None):
        """Load the trained weights
           useful if we are interested in using
                the network right away
        Arguments:
            actor_weights (string): filename containing actor net
                weights
            value_weights (string): filename containing value net
                weights
        """
        for model, i in zip(self.actor_models, self.output_count):
            model.load_weights(self.properties.gradient_model_folder + actor_weights + "_" + str(i) + ".h5")

        if value_weights is not None:
            self.value_model.load_weights(self.properties.gradient_model_folder + value_weights + ".h5")
