import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers


class AutoEncoder():
    def __init__(self, input_dim, latent_dim, save_path):
        inputs = keras.Input(shape=(input_dim,))
        self.save_path = save_path

        # encoder
        inputs = keras.Input(shape=(input_dim,))
        #x = layers.Dense(input_dim//2, activation="relu")(inputs)
        x = layers.Dense(input_dim, activation="relu")(inputs)
        x = layers.Dense(latent_dim, activation="relu")(x)

        # decoder
        x = layers.Dense(latent_dim, activation="relu")(x)
        #x = layers.Dense(input_dim//2, activation="relu")(x)
        outputs = layers.Dense(input_dim, activation="tanh")(x)

        self.model = keras.Model(
            inputs=inputs, outputs=outputs, name="autoencoder")
        self.model.summary()

        self.model.compile(
            optimizer='adam', loss=keras.losses.MeanSquaredError(), metrics=["accuracy"])

    def train(self, X, y):
        self.model.fit(np.array(X), np.array(y), shuffle=True, batch_size=128,
                       epochs=15, validation_split=0.2)

        self.model.save(self.save_path)
