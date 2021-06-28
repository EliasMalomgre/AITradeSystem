from os import path, mkdir

import numpy as np
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model

from ai.enviroment.environment import Environment
from properties.properties import Properties


class AutoEncoder:
    def __init__(self, state_dim, env: Environment):
        self.properties: Properties = Properties()
        self.state_dim = state_dim
        self.env = env
        self.encoder = None
        self.decoder = None
        self.auto_encoder = None

    def build_autoencoder(self):
        """Autoencoder to convert states into features
        """
        # first build the encoder model
        inputs = Input(shape=(self.state_dim,), name='state')
        feature_size = self.properties.encoder_feature_size
        x = Dense(256, activation='relu')(inputs)
        x = Dense(128, activation='relu')(x)
        feature = Dense(feature_size, name='feature_vector')(x)

        # instantiate encoder model
        self.encoder = Model(inputs, feature, name='encoder')
        self.encoder.summary()

        # build the decoder model
        feature_inputs = Input(shape=(feature_size,),
                               name='decoder_input')
        x = Dense(128, activation='relu')(feature_inputs)
        x = Dense(256, activation='relu')(x)
        outputs = Dense(self.state_dim, activation='linear')(x)

        # instantiate decoder model
        self.decoder = Model(feature_inputs,
                             outputs,
                             name='decoder')
        self.decoder.summary()

        # autoencoder = encoder + decoder
        # instantiate autoencoder model
        self.auto_encoder = Model(inputs,
                                  self.decoder(self.encoder(inputs)),
                                  name='autoencoder')
        self.auto_encoder.summary()

        # Mean Square Error (MSE) loss function, Adam optimizer
        self.auto_encoder.compile(loss='mse', optimizer='adam')

    def train_autoencoder(self):
        """Training the autoencoder using randomly sampled
            states from the environment
        Arguments:
            x_train (tensor): autoencoder train dataset
            x_test (tensor): autoencoder test dataset
        """
        x_train = [np.asarray(self.env.sample().to_array()) \
                   for _ in range(self.properties.encoder_sample_size)]
        x_train = np.array(x_train)
        x_test = [np.asarray(self.env.sample().to_array()) \
                  for _ in range(self.properties.encoder_sample_size)]
        x_test = np.array(x_test)

        # train the autoencoder
        batch_size = self.properties.encoder_batch_size
        self.auto_encoder.fit(x_train,
                              x_train,
                              validation_data=(x_test, x_test),
                              epochs=self.properties.encoder_train_epochs,
                              batch_size=batch_size)

    def load_encoder_weights(self, encoder_weights):
        """Load encoder trained weights
           useful if we are interested in using
            the network right away
        Arguments:
            encoder_weights (string): filename containing encoder net
                weights
        """
        self.encoder.load_weights(self.properties.encoder_model_folder + encoder_weights + ".h5")

    def save_encoder_weights(self, encoder_weights):
        """Save the actor, critic and encoder weights
            useful for restoring the trained models
        Arguments:
            actor_weights (tensor): actor net parameters
            encoder_weights (tensor): encoder weights
            value_weights (tensor): value net parameters
        """
        if not path.isdir(self.properties.encoder_model_folder):
            mkdir(self.properties.encoder_model_folder)

        self.encoder.save_weights(self.properties.encoder_model_folder + encoder_weights + ".h5")
