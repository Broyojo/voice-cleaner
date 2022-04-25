from autoencoder import AutoEncoder
import os
import struct
from alive_progress import alive_bar
from pathlib import Path


def main():
    ae = AutoEncoder(input_dim=22050, latent_dim=2205,
                     save_path="models/first_run.h5")

    X = []

    l = len(os.listdir("data/train/"))
    with alive_bar(l) as bar:
        for file in os.listdir("data/train/"):
            if file.endswith(".raw"):
                name = os.path.join("data/train/", file)

                data = Path(name).read_bytes()

                samples = []

                for i in range(0, len(data), 2):
                    sample = struct.unpack("h", data[i:i+2])
                    samples.append(sample[0] / 32767)

                if len(samples) == 22050:  # pad with zeros in the future
                    X.append(samples)
            bar()

    ae.train(X, X)


if __name__ == "__main__":
    main()
