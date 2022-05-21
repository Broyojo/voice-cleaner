from dataset import load_dataset, save_output
from keras import models
import numpy as np


def main():

    # this is actually unused. tf just gets angry when I do not define cfft_loss
    def cfft_loss(y_actual, y_pred):
        custom_loss = keras.metrics.mean_squared_error(keras.layers.Lambda(
            signal.rfft)(y_actual), keras.layers.Lambda(signal.rfft)(y_pred))
        return custom_loss

    X = np.array(load_dataset("data/test/", 1600))

    ae = models.load_model("models/minecraft_conv_49x_big_kernel.h5",
                           custom_objects={'cfft_loss': cfft_loss})

    pred = ae.predict(X)

    print(pred.shape)
    print(pred[0].shape)

    print(pred[0:30])

    pred *= 32767  # scale up

    print(pred[0:30])

    print("prediction shape:", pred[0].shape)

    save_output("data/output/", pred)


if __name__ == "__main__":
    main()
