import random

import numpy as np

from Service.IService import Service


class FactoryAutonomous(Service):
    def __init__(self,*args):
        super().__init__(*args)
        self._task_complexity = 0
        self._network_latency = 0
        # add weights for each parameter


    def calculate_arrival_rate(self):
        # TODO: add doc string

        return 3

    def calcualate_processing_time(self):
        # self._network_latency + self._task_complexity
        return np.random.choice(np.arange(12,15))
    def time_out(self):
        return np.random.choice(np.arange(32,38))

