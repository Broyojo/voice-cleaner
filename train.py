from autoencoder import AutoEncoder
from dataset import load_dataset


def main():
    ae = AutoEncoder(input_dim=22050, latent_dim=2205,
                     save_path="models/first_run.h5")

    X = load_dataset("data/train/")

    return

    ae.train(X, X)


if __name__ == "__main__":
    main()