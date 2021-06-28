from abc import ABC, abstractmethod
from os import path, mkdir

import numpy as np
import tensorflow_probability as tfp
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.layers import Lambda, Activation
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam, RMSprop

from ai.agent.episode import Episode
from ai.agent.percept import Percept
from ai.enviroment.environment import Environment
from ai.learning.learningstrategy import LearningStrategy
from ai.learning.policy_gradient.encoder import AutoEncoder
from properties.properties import Properties
from properties.simulation_type import SimulationType


class GradientMultipleOutputs(LearningStrategy, ABC):
    properties: Properties = Properties()

    def __init__(self, environment: Environment, λ=properties.gradient_λ, γ=properties.gradient_γ,
                 t_max=properties.gradient_t_max, outputs=properties.gradient_default_output_count if
            properties.simulator_simulation_type == SimulationType.ALL_ACTIONS else 3):
        super().__init__(environment, λ, γ, t_max)
        self.beta = self.properties.gradient_beta
        self.loss = self.value_loss

        self.memory: [Percept] = []
        self.state_dim = self.env.state_size
        self.state = self.env.reset().to_array()
        self.state = np.reshape(self.state, [1, self.state_dim])
        self.auto_encoder = AutoEncoder(self.state_dim, environment)
        self.outputs = outputs

        self.auto_encoder.build_autoencoder()
        if self.properties.encoder_train_autoencoder:
            self.auto_encoder.train_autoencoder()
            if self.properties.encoder_save_autoencoder:
                self.auto_encoder.save_encoder_weights(self.properties.encoder_weights)
        else:
            self.auto_encoder.load_encoder_weights(self.properties.encoder_weights)

        self.build_actor_critic()
        if self.properties.gradient_load_models:
            self.load_weights(self.properties.gradient_actor_model_weights,
                              self.properties.gradient_value_model_weights)

    @abstractmethod
    def next_action(self, state):
        state = np.reshape(state.to_array(), [1, self.state_dim])
        action = self.actor_model.predict(state)
        return action[0]

    @abstractmethod
    def learn(self, episode: Episode, **kwargs):
        super().learn(episode, **kwargs)

    @abstractmethod
    def start_episode(self):
        super().start_episode()

    def action(self, args):
        """Given means and stddevs, sample an action, clip
            and return
            We assume Gaussian distribution of probability
            of selecting an action given a state
        Argument:
            args (list) : means, stddevs
        Return:
            action (tensor): policy action
        """
        # Split incoming arg into means and stddevs
        means, stddevs = np.array_split(np.array(args), 2)

        actions = []

        # Apply Gaussian distribution for each mean and stddev pair
        for mean, stddev in zip(means, stddevs):
            dist = tfp.distributions.Normal(loc=mean, scale=stddev)
            action = dist.sample(1)
            action = K.clip(action,
                            0,
                            1)
            actions.append(action)
        return actions

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
        x = self.auto_encoder.encoder(inputs)
        mean = Dense(self.outputs,
                     activation='linear',
                     kernel_initializer='zero',
                     name='mean')(x)
        stddev = Dense(self.outputs,
                       kernel_initializer='zero',
                       name='stddev')(x)
        # use of softplusk avoids stddev = 0
        stddev = Activation('softplusk', name='softplus')(stddev)
        action = Lambda(self.action,
                        output_shape=(self.outputs,),
                        name='action')([mean, stddev])
        self.actor_model = Model(inputs, action, name='action')
        self.actor_model.summary()

        logp = Lambda(self.logp,
                      output_shape=(1,),
                      name='logp')([mean, stddev, action])
        self.logp_model = Model(inputs, logp, name='logp')
        self.logp_model.summary()

        entropy = Lambda(self.entropy,
                         output_shape=(1,),
                         name='entropy')([mean, stddev])
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
        optimizer = RMSprop(lr=self.properties.gradient_lr)
        self.logp_model.compile(loss=loss, optimizer=optimizer)

        optimizer = Adam(lr=self.properties.gradient_lr)
        self.value_model.compile(loss=self.loss, optimizer=optimizer)

    @staticmethod
    def logp(args):
        """Given mean, stddev, and action compute
            the log probability of the Gaussian distribution
        Argument:
            args (list) : mean, stddev action, list
        Return:
            logp (tensor): log of action
        """
        mean, stddev, action = args
        dist = tfp.distributions.Normal(loc=mean, scale=stddev)
        logp = dist.log_prob(action)
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
        mean, stddev = args
        dist = tfp.distributions.Normal(loc=mean, scale=stddev)
        entropy = dist.entropy()
        return entropy

    @staticmethod
    def logp_loss(entropy, beta=0.0):
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
            loss = -K.mean((y_pred * y_true) \
                           + (beta * entropy), axis=-1)
            return loss

        return loss

    @staticmethod
    def value_loss(y_true, y_pred):
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

        self.actor_model.save_weights(actor_weights + ".h5")

        if value_weights is not None:
            self.value_model.save_weights(value_weights)

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
        self.actor_model.load_weights(actor_weights + ".h5")

        if value_weights is not None:
            self.value_model.load_weights(value_weights)
