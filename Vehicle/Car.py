import random
import math

from Environment import env_variables
from Service.FactoryService import FactoryService
from Utils import config
from Vehicle.IVehicle import Vehicle
from Utils.config import SERVICES_TYPES


class Car(Vehicle):
    def car_requests(self):
        self.services = []
        car_services = []
        types = [*SERVICES_TYPES.keys()]
        # print("...... ",types)
        # print("env_variables.ENTERTAINMENT_RATIO : " ,env_variables.ENTERTAINMENT_RATIO)
        type_=random.choices(types,weights=(env_variables.ENTERTAINMENT_RATIO,env_variables.SAFETY_RATIO,env_variables.AUTONOMOUS_RATIO), k=1)
        # print("choosen type : ",type_)
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

        car_request_tuple = self.car_requests()[0]
        # print("car_request_tuple : ", car_request_tuple)
        # print(" self.outlets_serve : ", self.outlets_serve)
        #
        # filtered_realtime = dict(filter(lambda item: int(min(item[1])) >= int(car_request_tuple[2].realtime),
        #                                 config.REALTIME_BANDWIDTH.items()))
        # names = [i.__class__.__name__ for i in self.outlets_serve]
        # names = set(names)
        # filtered_realtime_names = [i[0] for i in filtered_realtime.items()]
        # common_elements = names.intersection(filtered_realtime_names)
        # temp = common_elements.pop()
        # common_elements.add(temp)
        #
        # if len(common_elements) == 1 and list(common_elements)[0] == 'Satellite':
        #     return self.outlets_serve[-1], car_request_tuple
        # else:
        #     list_outlet_to_make_greedy_on = list(
        #         filter(lambda item: list(common_elements)[0] == item.__class__.__name__, self.outlets_serve))
        #
        distance = list(map(lambda x: euclidian_distance(x), self.outlets_serve))
        # print("distance : ", distance)
        if len(distance)==0:
            return None, None
        else :
            # print("self.outlets_serve[distance.index(min(distance))] :  ", self.outlets_serve[distance.index(min(distance))])
            # print("min distance : ", min(distance))
            # print("self.outlets_serve : ", self.outlets_serve)
            # print("self.outlets_serve[distance.index(min(distance))]  : " ,self.outlets_serve[distance.index(min(distance))])
            return self.outlets_serve[distance.index(min(distance))], car_request_tuple
        # return self.outlets_serve[-1], car_request_tuple
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
            del outlet.services
            outlet.services = []
            outlet.services.extend([outlet, request])
            del request
            return outlet.services
        else :
            return None
