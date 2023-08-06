import numpy as np


class GridCell:
    _services_ensured: np.ndarray
    _services_requested: np.ndarray

    def __init__(self):
        self._services_requested = np.zeros(3)
        self._services_ensured = np.zeros(3)
        self._occupancy = 0
        self._utility = 0
        self.power_allocated = np.zeros(3)
        self.grid_outlets = []
        self.outlets_id = []

    @property
    def services_ensured(self):
        return self._services_ensured

    @services_ensured.setter
    def services_ensured(self, serv):
        self._services_ensured = np.array(serv)

    @property
    def services_requested(self):
        return self._services_requested

    @services_requested.setter
    def services_requested(self, serv):
        self._services_requested = np.array(serv)

    @property
    def utility(self):
        return self._utility

    @utility.setter
    def utility(self, u):
        self._utility = u

    @property
    def occupancy(self):
        return self._occupancy

    @occupancy.setter
    def occupancy(self, o):
        self._occupancy = o
