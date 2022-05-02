from alive_progress import alive_bar
import os
from pathlib import Path
import struct
import re

# alphanumeric sorted data


def sorted_alphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()
    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def load_dataset(path, n_samples, max_files=0):
    tracks = []
    ls = [s for i, s in enumerate(os.listdir(
        path)) if i < max_files or max_files == 0]
    with alive_bar(len(ls), dual_line=True, title="Loading Dataset...") as bar:
        for file in sorted_alphanumeric(ls):
            if file.endswith(".raw"):
                name = os.path.join(path, file)
                bar.text = f"Loading {name}..."
                data = Path(name).read_bytes()
                samples = []
                for i in range(0, len(data), 2):
                    # read two bytes at a time
                    sample = struct.unpack("h", data[i:i+2])
                    # normalize audio between 0 and 1
                    samples.append(sample[0] / 32767)
                # pad with zeros in the future
                # and any([round(s * 32767) != 0 for s in samples]):
                if len(samples) == n_samples:
                    tracks.append(samples)
            bar()
        bar.title = "Loading Dataset... Done!"
    return tracks


def clamp(x, a, b):
    if x < a:
        return a
    elif x > b:
        return b
    return x


def save_output(path, data):
    with alive_bar(len(data), dual_line=True, title="Saving Output...") as bar:
        for s, sample in enumerate(data):
            name = os.path.join(path, f"{s}.raw")
            with open(name, "wb") as f:
                for i in range(len(sample)):
                    y = round(sample[i])
                    y = clamp(y, -32767, 32767)
                    data = struct.pack("h", y)
                    f.write(data)
            bar()
        bar.title = "Saving Output... Done!"
