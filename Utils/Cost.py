import os

from Utils.Bandwidth import Bandwidth
from dotenv import load_dotenv
import os
from Utils import config as cf
from Utils.FileLogging import log_method

load_dotenv()


class Cost:
    _cost: float

    def __init__(self, bandwidth: Bandwidth, realtime: int) -> None:
        self.realtime = realtime
        self.bit_rate = bandwidth.allocated
        self._cost = self.bit_rate

    @property
    def cost(self):
        return self._cost

    def cost_setter(self, outlet):
        cost = self.bit_rate
        if outlet.__class__.__name__ == "Wifi":
            # print("....  wifi")
            cost = self.bit_rate
        elif outlet.__class__.__name__ == "ThreeG":
            # print("....  3G")
            cost = self.bit_rate * 1.1
        elif outlet.__class__.__name__ == "FourG":
            # print("....  4G")
            cost = self.bit_rate * 1.3
        elif outlet.__class__.__name__ == "FiveG":
            # print("....  5G")
            cost = self.bit_rate * 1.5
        elif outlet.__class__.__name__ == "Satellite":
            print("....  SAT")
            cost = self.bit_rate * 2
        return cost

    # def __str__(self):
    #     raise NotImplementedError()


class RequestCost(Cost):
    @property
    def cost(self):
        cost = self._cost * float(os.getenv("MB_COST"))
        # self.logger.log(f"RequestCost: {cost}")
        return f"{cost:.2f}"

    @cost.setter
    def cost(self, value):
        self._cost = self.cost_setter(value)

    # def __str__(self):
    #     fee = self._cost * float(os.getenv("MB_COST"))
    #     return f'Request Fee: {fee}'


class TowerCost(Cost):
    @property
    def cost(self):
        cost = self._cost * float(os.getenv("KW_COST"))
        return cost

    @cost.setter
    def cost(self, value):
        self._cost = self.cost_setter(value)

    # def __str__(self):
    #     return f'Request Fee: {self.cost}'
