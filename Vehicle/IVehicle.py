from abc import ABC
from Environment import env_variables
from typing import List

import traci


class Vehicle(ABC):
    # TODO: replace int with road object in annotation
    def __init__(self, id_, x : float , y : float, **kwargs):
        """
        Parameters
        ----------
         speed : float
            The frequency used by the service.
         position : list
            x,y coordinates of the vehicle in the environment
         acceleration : float
            at how mush rate the vehicle increments it's speed
         path : list[Road]
             roads path of the vehicle
         services : list[Service]

        """

        self.id = id_
        self.services = []
        self.outlets_serve = []
        self.observers = []
        self.x = x
        self.y = y


    def check_position(self):
        self.x = float(round(traci.vehicle.getPosition(self.id)[0],4))
        self.y = float(round(traci.vehicle.getPosition(self.id)[1],4))

    def get_x(self):
        self.check_position()
        return self.x

    def get_y(self):
        self.check_position()
        return self.y
