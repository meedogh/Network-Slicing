from abc import ABC, abstractmethod
from typing import Tuple
from collections import deque

from RL.RLBuilder import RLBuilder
from RL.RLEnvironment.Action.ActionResponse import ActionResponse
from RL.RLEnvironment.State.DecentralizedState import DeCentralizedState
from RL.RLEnvironment.Reward.DecentralizedReward import DeCentralizedReward


class Outlet(ABC):
    """
    Definition of coverage towers
    """

    __id = -1

    def __init__(
            self,
            id_,
            position: Tuple[float],
            radius: float,
            power: [float],
            requests_allocated_power: [float],

    ):
        """
        Parameters
        ----------
        position : Tuple[float]
            The coordinates of the outlet.
        radius : float
            The radius of the coverage area.
        power : [float]
            The power or the outlet.

            """
        self.__class__.__id += 1

        self._distinct = self.__class__.__id
        self.id_ = id_
        self.position = position
        self._radius = radius
        self._power = power  # bit rate
        self.requests_allocated_power = requests_allocated_power
        self._power_distinct = []
        self.request_buffer = []
        self._occupancy = 0
        self._utility = 0
        self._sum_of_service_requested_power_allocation = 0
        self._services_requested = [0, 0, 0]
        self._services_ensured = [0, 0, 0]
    @property
    def raduis(self):
        return self._radius
    @raduis.setter
    def raduis(self,r):
        self._radius=r
    @property
    def services_ensured(self):
        return self._services_ensured

    @services_ensured.setter
    def services_ensured(self, serv):
        self._services_ensured = serv
    @property
    def services_requested(self):
        return self._services_requested
    @services_requested.setter
    def services_requested(self,serv):
        self._services_requested = serv
    @property
    def utility(self):
        return self._utility

    @utility.setter
    def utility(self, u):
        self._utility = u

    @property
    def outlet_id(self):
        return self.id_

    @outlet_id.setter
    def outlet_id(self, i):
        self.id_ = i

    @property
    def occupancy(self):
        return self._occupancy

    @occupancy.setter
    def occupancy(self, o):
        self._occupancy = o

    @property
    def sum_of_service_requested_power_allocation(self):
        return self._sum_of_service_requested_power_allocation

    @sum_of_service_requested_power_allocation.setter
    def sum_of_service_requested_power_allocation(self, s):
        self._sum_of_service_requested_power_allocation = s

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value

    @property
    def distinct(self):
        return self._distinct

    @distinct.setter
    def distinct(self, d):
        self._distinct = d

    @abstractmethod
    def calculate_coverage_area(self):
        """Returns
        -------
        nothing , it is an abstract method
           The coverage area that the tower will response the requests in it."""
        pass

    @abstractmethod
    def calculate_downlink(self):
        """Returns
        -------
        nothing , it is an abstract method
           The downlink that the tower will use it for responsing the requests ."""
        pass

    @property
    def power_distinct(self):
        return [self._power, self._distinct]

