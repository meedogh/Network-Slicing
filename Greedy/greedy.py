import numpy as np
import copy


class Greedy:
    def __init__(self):
        self.num_services = 3
        self._supported_services = [1, 1, 1]
        self._services_ensured = np.zeros(self.num_services)
        self._services_requested = np.zeros(self.num_services)
        self.request_response_reject = 1

