from dataset import load_dataset, save_output
from keras import models
import numpy as np


def main():
    X = np.array(load_dataset("data/test/", 2205))

    ae = models.load_model("models/minecraft.h5")

    pred = ae.predict(X)

    print(pred[0:30])

    pred *= 32767  # scale up

    print(pred[0:30])

    print("prediction shape:", pred[0].shape)

    save_output("data/output/", pred)


if __name__ == "__main__":
    main()
