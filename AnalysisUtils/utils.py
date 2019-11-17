import pandas as pd
import matplotlib.pyplot as plt
import typing as tp
import seaborn as sns
import numpy as np


class WordUniqueness:
    def __init__(self):
        self.uniqueness = pd.read_csv("inverse_frequencies.csv", index_col=0, header=None).to_dict()

    def calculate_idfs(self, text: str):
        idfs = []
        for word in text.split():
            if word in self.uniqueness:
                idfs.append(self.uniqueness[word])
        return idfs

    def calculate_uniqueness(self, text):
        return np.mean(self.calculate_idfs(text))
