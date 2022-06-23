from models import LinearAutoEncoder, ConvolutionalAutoEncoder
from dataset import load_dataset


def main():
    n_samples = 2205

    # ae = LinearAutoEncoder(input_dim=n_samples, latent_dim=n_samples,
    #                        save_path="models/minecraft_nocompression.h5")

    ae = ConvolutionalAutoEncoder(
        input_dim=n_samples, compression_size=15, save_path="models/minecraft_denoise.h5")

    max_files = 50_000

    X = load_dataset("data/train/", n_samples, max_files)
    y = load_dataset("data/train_compressed/", n_samples, max_files)

    ae.train(X, y)


if __name__ == "__main__":
    main()
