# Voice Cleaner

## Description
This is an app that uses convolutional and linear autoencoders to remove noise from audio and to make voice sound more clean. This is mainly meant to upscale audio from phone calls, as those are quite compressed and noisy depending on how bad the signal is. The model is trained to turn low quality, noisy voice audio to high quality voice audio.

## Future Plans
In the future, we will try to make the model more accurate, as it tends to not be accurate in reducing noise when the audio is too noisy. We could do this by using a diffusion model to upscale audio in a similar way to how images are iteratively denoised. We also plan to have this model run on a phone so that people can use it to get better quality phone calls. 

## How To Run It
You must have `sox` and `ffmpeg` installed before running this app.

To install the Python dependencies, either run `pipenv install` or `pip install -r requirements.txt` depending on if you use [`pipenv`](https://pipenv.pypa.io/en/latest/) or `pip`.

Use the provided scripts to combine, compress, split, and convert audio. Then, use `train.py` and `test.py` to train and test the model respectively. Make sure to modify the paths as well as sampling rate in the script to match your training and testing data.

## Examples
This splits audio.wav in 0.05s sections and compresses each one. Then we train the model and test the model.
```
$ ./compressparal.sh -t 0.05 audio.wav
$ python3 train.py
$ python3 test.py
```