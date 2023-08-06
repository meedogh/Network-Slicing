import numpy as np


class Statistics:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def mean(data):
        return np.mean(data, axis=0)

    @staticmethod
    def std(data):
        return np.std(data, axis=0)

    @staticmethod
    def percentile(data, p):
        return np.percentile(data, p, axis=0)

    @staticmethod
    def min(data):
        return np.min(data, axis=0)

    @staticmethod
    def max(data):
        return np.max(data, axis=0)

    @staticmethod
    def range(data):
        return Statistics.max() - Statistics.min()

    """def summary(data):
        return {
            "mean": self.mean(),
            "std": self.std(),
            "percentile_25": self.percentile(25),
            "percentile_50": self.percentile(50),
            "percentile_75": self.percentile(75),
            "min": self.min(),
            "max": self.max(),
            "range": self.range()
        }"""
