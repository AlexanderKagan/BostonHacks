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




def pad_vectors(samples, max_len):
  new_vectors = []
  for elem in samples:
    vector = np.zeros(max_len)
    vector[:len(elem)] = elem
    new_vectors.append(vector)
  return np.array(new_vectors)

def prepare_data():
    labels, samples = [], []

    for folder in tqdm.tqdm(glob.glob("Actor_*")):
        for name in (glob.glob(folder + "/*.wav")):
            nm = name[name.find('/') + 1:name.rfind(".")].split('-')
            if nm[0] == '03' and nm[1] == '01':
                try:
                    if nm[2] in ['01', '02']:
                        label = 0
                    elif nm[2] in ['03', '08']:
                        label = 1
                    else:
                        label = -1
                    sample, freq = librosa.load(name, 16000)
                    samples.append(sample)
                    labels.append(label)
                except:
                    pass

    max_len = np.max(list(map(len, samples)))
    padded_vects = pad_vectors(samples, max_len)
    mean, std = padded_vects.mean(axis=0), padded_vects.std(axis=0)
    padded_vects = (padded_vects - mean) / std
    new_targets = (np.array(labels) >= 0) * 1
    return padded_vects, new_targets, (mean, std)

def samples_and_labels_generator(batch_size, padded_vects, new_targets):
    max_size = len(padded_vects)
    while True:
        inds = np.random.choice(max_size, batch_size)
        batch_images = padded_vects[inds]
        batch_labels = new_targets[inds]
        yield batch_images, batch_labels


def train_iterator(batch_size, padded_vects, new_targets):
    for batch in samples_and_labels_generator(batch_size, padded_vects, new_targets):
        samples = batch[0].astype('float32')
        samples = np.expand_dims(samples, -1)
        labels = keras.utils.to_categorical(batch[1], 2)
        yield samples, labels

# reset graph when you change architecture!
def reset_tf_session():
    curr_session = tf.get_default_session()
    # close current session
    if curr_session is not None:
        curr_session.close()
    # reset graph
    K.clear_session()
    # create new session
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    s = tf.InteractiveSession(config=config)
    K.set_session(s)
    return s


def make_model(max_len):
    """
    Define your model architecture here.
    Returns `Sequential` model.
    """
    model = Sequential()

    model.add(Conv1D(4, 4, padding='same', activation='elu', input_shape=(max_len, 1)))
    model.add(MaxPooling1D(4))

    model.add(Conv1D(8, 4, padding='same', activation='elu'))
    model.add(MaxPooling1D(4))

    model.add(Conv1D(16, 4, padding='same', activation='elu'))
    model.add(MaxPooling1D(4))

    model.add(Conv1D(32, 4, padding='same', activation='elu'))
    model.add(MaxPooling1D(4))

    model.add(Conv1D(64, 4, padding='same', activation='elu'))
    model.add(MaxPooling1D(4))

    model.add(Conv1D(128, 4, padding='same', activation='elu'))
    model.add(MaxPooling1D(4))

    model.add(Conv1D(256, 4, padding='same', activation='elu'))
    model.add(MaxPooling1D(4))

    model.add(GlobalAveragePooling1D())

    model.add(Dense(64, activation='elu'))
    model.add(Dense(2, activation="softmax"))

    return model


if __name__ == "__main__":
    padded_vects, new_targets, (mean, std) = prepare_data()

    s = reset_tf_session()
    model = make_model(padded_vects.shape[1])

    BATCH_SIZE = 5
    STEPS_PER_EPOCH = 250
    EPOCHS = 7

    model.compile(
        loss='binary_crossentropy',
        optimizer=keras.optimizers.adam(clipnorm=5.),
        metrics=[categorical_accuracy]
    )

    model.fit_generator(
        train_iterator(BATCH_SIZE),
        steps_per_epoch=STEPS_PER_EPOCH,
        epochs=EPOCHS,
        verbose=1
    )

