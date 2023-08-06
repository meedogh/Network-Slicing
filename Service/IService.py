from abc import ABC, abstractmethod


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
        self._processing_time = 0
        self._dec_services_types_mapping= {"FactorySafety":0,"FactoryEntertainment":1,"FactoryAutonomous":2}

    # def __str__(self):
    #     return f"service criticality : {self.criticality} ,  service bandwidth : {self.bandwidth} , " \
    #            f"service real time : {self.realtime}"

    def request_supported(self,outlet):
        # print("outlet.dqn.environment.state.supported_services  : ", outlet.dqn.environment.state.supported_services)
        if self.__class__.__name__=='FactorySafety':
            if outlet.dqn.environment.state.supported_services[0] == 1 :
                return True
            else :
                return False
        elif self.__class__.__name__=='FactoryEntertainment':
            if outlet.dqn.environment.state.supported_services[1] == 1 :
                return True
            else :
                return False
        elif self.__class__.__name__=='FactoryAutonomous':
            if outlet.dqn.environment.state.supported_services[2] == 1 :
                return True
            else :
                return False
    @property
    def processing_time(self):
        return self._processing_time
    @processing_time.setter
    def processing_time(self,value):
        self._processing_time = value
    @property
    def service_power_allocate(self):
        return self._service_power_allocate

    @service_power_allocate.setter
    def service_power_allocate(self,value):
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

    @abstractmethod
    def calcualate_processing_time(self):
        pass
