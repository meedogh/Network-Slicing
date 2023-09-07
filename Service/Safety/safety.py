from Service.IService import Service
import numpy as np

class FactorySafety(Service):
    def __init__(self,*args):
        super().__init__(*args)
        self._task_complexity = 0
        self._network_latency = 0
        # add weights for each parameter

    def calcualate_processing_time(self):
        # self._network_latency + self._task_complexity
        return np.random.choice(np.arange(10,18))

    def time_out(self):
        return np.random.choice(np.arange(2,4))
    def calculate_arrival_rate(self):
        # TODO: add doc string

        return 2
