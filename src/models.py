import numpy as np
from tensorflow import keras
from tensorflow import signal
from keras import activations
from keras import layers
#import dpam


class ConvolutionalAutoEncoder:
    def __init__(self, input_dim, compression_size, save_path):
        self.save_path = save_path

        def cfft_loss(y_actual, y_pred):
            custom_loss = keras.metrics.mean_squared_error(keras.layers.Lambda(
                signal.rfft)(y_actual), keras.layers.Lambda(signal.rfft)(y_pred))
            return custom_loss

        def dpam_loss(y_actual, y_pred):
            loss_fn = dpam.DPAM()
            dist = loss_fn.forward(y_actual, y_pred)
            return custom_loss
        # Encoder

        encoder_input = keras.Input(
            shape=(input_dim, 1), name="original_image")

        x = layers.Conv1D(
            filters=16,
            kernel_size=35,
            strides=1,
            activation=activations.elu,
            padding='causal',
        )(encoder_input)

        x = layers.Conv1D(
            filters=32,
            kernel_size=35,
            strides=1,
            activation=activations.elu,
            padding='causal',
        )(x)

        encoder_output = layers.MaxPooling1D(pool_size=compression_size)(x)

        self.encoder = keras.Model(
            encoder_input, encoder_output, name="encoder")

        self.encoder.summary()

        # Decoder

        decoder_input = keras.Input(
            shape=(input_dim//compression_size, 32), name="encoded_image")

        x = layers.UpSampling1D(size=compression_size)(decoder_input)

        x = layers.Conv1DTranspose(
            filters=32,
            kernel_size=35,
            strides=1,
            activation=activations.elu,
            padding='same',
        )(x)

        x = layers.Conv1D(
            filters=16,
            kernel_size=35,
            strides=1,
            activation=activations.elu,
            padding='causal',
        )(x)

        decoder_output = layers.Conv1DTranspose(
            filters=1,
            kernel_size=35,
            strides=1,
            activation=activations.tanh,
            padding='same',
        )(x)

        self.decoder = keras.Model(
            decoder_input, decoder_output, name="decoder")

        self.decoder.summary()

        # Autoencoder
        autoencoder_input = keras.Input(shape=(input_dim, 1), name="image")
        encoded_image = self.encoder(autoencoder_input)
        decoded_image = self.decoder(encoded_image)
        self.autoencoder = keras.Model(
            autoencoder_input, decoded_image, name="autoencoder")
        self.autoencoder.summary()

        self.autoencoder.compile(
            optimizer=keras.optimizers.Adam(epsilon=1e-06), loss=cfft_loss, metrics=["accuracy"])  # Adjust loss

    def train(self, X, y):
        self.autoencoder.fit(np.array(X), np.array(y), shuffle=True,
                             batch_size=128, epochs=7, validation_split=0.2)

        self.autoencoder.save(self.save_path)


class LinearAutoEncoder:
    def __init__(self, input_dim, latent_dim, save_path):
        inputs = keras.Input(shape=(input_dim,))
        self.save_path = save_path

        # encoder
        inputs = keras.Input(shape=(input_dim,))
        x = layers.Dense(input_dim, activation="relu")(inputs)
        x = layers.Dense(latent_dim, activation="relu")(x)

        # decoder
        x = layers.Dense(latent_dim, activation="relu")(x)
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
