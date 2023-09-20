import random
import math

from Environment import env_variables
from Service.FactoryService import FactoryService
from vehicle.IVehicle import Vehicle
from Utils.config import SERVICES_TYPES


class Car(Vehicle):
    def car_requests(self):
        self.services = []
        car_services = []
        types = [*SERVICES_TYPES.keys()]
        type_=random.choices(types,weights=(env_variables.ENTERTAINMENT_RATIO,env_variables.SAFETY_RATIO,env_variables.AUTONOMOUS_RATIO), k=1)
        realtime_ = random.choice(SERVICES_TYPES[type_[0]]["REALTIME"])
        bandwidth_ = random.choice(SERVICES_TYPES[type_[0]]["BANDWIDTH"])
        criticality_ = random.choice(SERVICES_TYPES[type_[0]]["CRITICAL"])

        factory = FactoryService(realtime_, bandwidth_, criticality_)
        service_ = factory.produce_services(type_[0])
        service_.realtime = realtime_

        self.services.append(service_)
        car_services = list(map(lambda x: [self.get_id(), self, x], self.services))
        del self.services

        return car_services
        # return None

    def get_id(self):
        return self.id

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)

    def set_state(self, x, y):
        self.x = x
        self.y = y
        self.notify()

    def greedy(self):
        def euclidian_distance(outlet):
            result = math.sqrt(
                (outlet.position[0] - self.x) ** 2 + (outlet.position[1] - self.y) ** 2
            )
            return result

        def get_smallest_indices(arr):
            sorted_indices = sorted(range(len(arr)), key=lambda i: arr[i])
            return sorted_indices[:2]

        car_request_tuple = self.car_requests()[0]
        distance = list(map(lambda x: euclidian_distance(x), self.outlets_serve))
        if len(distance) == 0:
            return None, None
        else:
            indices = get_smallest_indices(distance)
            # min1 = distance.index(min(distance))
            if len(distance) == 1:
                # print("choice 1 :  " , self.outlets_serve[indices[0]] )
                return [self.outlets_serve[indices[0]]], car_request_tuple
            if len(distance) > 1:
                # print("choice 2 : " , self.outlets_serve[indices[0]] )
                return [self.outlets_serve[indices[0]],self.outlets_serve[indices[1]]], car_request_tuple

    def check_outlet_types(self, outlet, type):
        if outlet.__class__.__name__ == type:
            return True
        else:
            return False

    def add_satellite(self, satellite):
        if satellite not in self.outlets_serve:
            self.outlets_serve.append(satellite)

    def send_request(self):
        outlet, request = self.greedy()
        if outlet != None :
            return [outlet, request]
        else :
            return None
