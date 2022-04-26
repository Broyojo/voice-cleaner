from autoencoder import AutoEncoder
from dataset import load_dataset


def main():
    n_samples = 2205

    ae = AutoEncoder(input_dim=n_samples, latent_dim=n_samples //
                     5, save_path="models/classical_50ms.h5")

    X = load_dataset("data/train/", n_samples)

    ae.train(X, X)


if __name__ == "__main__":
    main()
