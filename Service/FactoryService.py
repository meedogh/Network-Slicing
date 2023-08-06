from Service.Entertainment.Entertainment import FactoryEntertainment
from Service.Safety.safety import FactorySafety
from Service.Autonomous.autonomous import FactoryAutonomous


# noinspection PyAbstractClass
class FactoryService:
    def __init__(self, *args):
        """
        *args: params
            Service init parameters; reference to Iservice.py
        """

        self.entertainment = FactoryEntertainment(*args)
        self.safety = FactorySafety(*args)
        self.telecom = FactoryAutonomous(*args)
        self.var = {"ENTERTAINMENT": self.entertainment,
                    "SAFETY": self.safety,
                    "AUTONOMOUS": self.telecom}

    def produce_services(self, product):
        if product in self.var.keys():
            return self.var[product]
        raise Exception(f'{product} factory not available at the moment!')
