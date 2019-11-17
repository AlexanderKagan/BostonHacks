import librosa
import numpy as np
import keras

model = keras.models.load_model("./super_model.h5")


def make_prediction(arr):
    a = 84351
    preds = []
    rem = (a - len(arr) % a) if len(arr) % a != 0 else 0
    new_arr = np.zeros(len(arr) + rem)
    new_arr[:len(arr)] = arr
    for i in range(0, len(new_arr) // a):
        preds.append(model.predict(np.expand_dims(new_arr[i * a: (i + 1) * a].reshape(1, -1), -1))[0][0])
    return np.mean(preds)


def predict_nerv():
    arr, _ = librosa.load("../record.wav", 16000)
    return make_prediction(arr)


if __name__ == "__main__":
    print(predict_nerv())
