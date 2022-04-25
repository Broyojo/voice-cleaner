from keras import models
from pathlib import Path
import struct
from alive_progress import alive_bar
import os
import numpy as np


def main():
    X = []

    l = len(os.listdir("data/test/"))
    with alive_bar(l) as bar:
        for file in os.listdir("data/test/"):
            if file.endswith(".raw"):
                name = os.path.join("data/test/", file)

                data = Path(name).read_bytes()

                samples = []

                for i in range(0, len(data), 2):
                    sample = struct.unpack("h", data[i:i+2])
                    samples.append(sample[0] / 32767)

                if len(samples) == 22050:
                    X.append(samples)
            bar()

    ae = models.load_model("models/first_run.h5")

    X = np.array(X)

    print(X[0])

    pred = ae.predict(X)

    pred *= 32767

    print("prediction shape:", pred[0].shape)

    for s, sample in enumerate(pred):
        with open(f"data/output/{s}.raw", "wb") as f:
            for i in range(len(sample)):
                data = struct.pack("h", round(sample[i]))
                f.write(data)


if __name__ == "__main__":
    main()
