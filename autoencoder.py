import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers


class AutoEncoder():
    def __init__(self, input_dim, latent_dim, save_path):
        inputs = keras.Input(shape=(input_dim,))
        self.save_path = save_path

        inputs = keras.Input(shape=(input_dim,))
        self.encoder = layers.Dense(latent_dim, activation="relu")
        x = self.encoder(inputs)

        decoder = layers.Dense(latent_dim, activation="sigmoid")
        x = decoder(x)
        outputs = layers.Dense(input_dim)(x)

        self.model = keras.Model(
            inputs=inputs, outputs=outputs, name="autoencoder")
        self.model.summary()

        self.model.compile(
            optimizer='adam', loss=keras.losses.MeanSquaredError(), metrics=["accuracy"])

    def train(self, X, y):
        self.model.fit(np.array(X), np.array(y), shuffle=True, batch_size=32,
                       epochs=32, validation_split=0.2)

        self.model.save(self.save_path)
