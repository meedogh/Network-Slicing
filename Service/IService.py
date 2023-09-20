from abc import ABC, abstractmethod

import numpy as np
import Utils.config as cf


class Service(ABC):

    def __init__(self, criticality, bandwidth, realtime, **kwargs):
        """
            Parameters
            ----------
            frequency : float
                The frequency used by the service.
            spectrum : float
                Represents the collection of frequencies that make up a signal and their relative strengths.
            data_rate : float
                The data rate of the service
            energy_consumption : float
                The energy consumed by the service
            transition_delay : float
                The transition delay of the service
            communications : list[Communication]
                The communications that supported the service if not initialized set to empty array to be appended at runtime

            """
        self.bandwidth = bandwidth
        self.criticality = criticality
        self._realtime = realtime
        self._service_power_allocate = 0
        self._dec_services_types_mapping = {"FactorySafety": 0, "FactoryEntertainment": 1, "FactoryAutonomous": 2}
        self.__id = +1
        self._time_out = 0
        self._time_execution = 0
        self.request_failure = False
        self.cost_in_bit_rate = 0
        self.total_cost_in_dolars = 0
        self.remaining_time_out = 0


    # def __str__(self):
    #     return f"service criticality : {self.criticality} ,  service bandwidth : {self.bandwidth} , " \
    #            f"service real time : {self.realtime}"
    def request_level_failure(self):
        random_failure_value = np.random.rand()
        if random_failure_value < 0.9:
            return True
        else:
            return False


    def calculate_service_cost_in_Dolar_per_bit(self):
        if self.__class__.__name__ == "FactoryEntertainment":
            return cf.CostForBitOfENTERTAINMENT * self.cost_in_bit_rate
        elif self.__class__.__name__ == "FactorySafety":
            return cf.CostForBitOfSAFETY * self.cost_in_bit_rate
        elif self.__class__.__name__ == "FactoryAutonomous":
            return cf.CostForBitOfAUTONOMOUS * self.cost_in_bit_rate




    def request_supported(self, outlet):
        # print("outlet.dqn.environment.state.supported_services  : ", outlet.dqn.environment.state.supported_services)
        if self.__class__.__name__ == 'FactorySafety':
            if outlet.dqn.environment.state.supported_services[0] == 1:
                return True
            else:
                return False
        elif self.__class__.__name__ == 'FactoryEntertainment':
            if outlet.dqn.environment.state.supported_services[1] == 1:
                return True
            else:
                return False
        elif self.__class__.__name__ == 'FactoryAutonomous':
            if outlet.dqn.environment.state.supported_services[2] == 1:
                return True
            else:
                return False

    @property
    def time_execution(self):
        return self._time_execution

    @time_execution.setter
    def time_execution(self, value):
        self._time_execution = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    @property
    def service_power_allocate(self):
        return self._service_power_allocate

    @service_power_allocate.setter
    def service_power_allocate(self, value):
        self._service_power_allocate = value

    @abstractmethod
    def calculate_arrival_rate(self):
        """ the rate at which messages or packets are received by a system or a network over a period of time """
        pass

    @property
    def realtime(self):
        return self._realtime

    @realtime.setter
    def realtime(self, r):
        self._realtime = r

    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, r):
        self.__id = r

    @abstractmethod
    def calculate_processing_time(self):
        pass
    @abstractmethod
    def calculate_time_out(self):
        pass
