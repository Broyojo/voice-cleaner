from autoencoder import AutoEncoder
from dataset import load_dataset


def main():
    n_samples = 2205

    ae = AutoEncoder(input_dim=n_samples, latent_dim=n_samples //
                     30, save_path="models/minecraft.h5")

    X = load_dataset("data/train/", n_samples, max_files=100_000)

    ae.train(X, X)


if __name__ == "__main__":
    main()
