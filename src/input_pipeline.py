import tensorflow as tf
from models import ConvolutionalAutoEncoder
import numpy as np
import struct

NUM_EPOCHS = 15
BATCH_SIZE = 128


files = tf.data.Dataset.list_files("data/train/*")
dataset = tf.data.TFRecordDataset(
    files, num_parallel_reads=16).shuffle(1000).repeat(NUM_EPOCHS).map(lambda x: tf.io.parse_tensor(x, out_type=tf.int16)).batch(BATCH_SIZE)

ae = ConvolutionalAutoEncoder(
    input_dim=1600, compression_size=32, save_path="models/new_input_pipeline.h5")


for batch in dataset:
    ae.autoencoder.fit(batch, batch)

ae.autoencoder.save(ae.save_path)
