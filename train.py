from models import LinearAutoEncoder, ConvolutionalAutoEncoder
from dataset import load_dataset


def main():
    n_samples = 1600

    # ae = LinearAutoEncoder(input_dim=n_samples, latent_dim=n_samples,
    #                        save_path="models/minecraft_nocompression.h5")

    ae = ConvolutionalAutoEncoder(
        input_dim=n_samples, compression_size=32, save_path="models/minecraft_conv_49x_big_kernel.h5")

    X = load_dataset("data/train/", n_samples, max_files=68_000)

    ae.train(X, X)


if __name__ == "__main__":
    main()
