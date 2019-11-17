import glob
import tqdm
import librosa
import numpy as np
import tensorflow as tf
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Activation, Dropout, GlobalAveragePooling1D, \
    BatchNormalization, LSTM, Bidirectional

from keras.metrics import categorical_accuracy


if __name__ == "__main__":
    pass
