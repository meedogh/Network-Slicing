from abc import abstractmethod
from collections import deque

from Communications.IComs import Communications
from Outlet.IOutlet import Outlet
import numpy as np

from RL.RLBuilder import RLBuilder
from RL.RLEnvironment.Action.ActionResponse import ActionResponse
from RL.RLEnvironment.Reward.DecentralizedReward import DeCentralizedReward
from RL.RLEnvironment.State.DecentralizedState import DeCentralizedState
from Utils.config import outlet_types


# noinspection PyAbstractClass
class Cellular(Outlet):
    """
    outlet from type cellular is the abstract class for different types ground towers
    """

    _max_capacity: float
    _current_capacity: float

    def __init__(
        self, tower, agent, coms: Communications, supported_services, *args, **kwargs
    ):
        """
        Parameters
        ----------
        agent : Agent
            RL agent from type outlet agent.
        coms : Communications
            the communication that will take the request to the outlet .
        supported_services : [bool]
            services that will the vehicle send it to outlet .
        services_list : [Services]
            services that will the vehicle send it to outlet (the outlet will responsed to it).
        vehicles_list : [Vehicles]
            The vehicles that demand a service from this outlet.

        """

        super().__init__(*args)

        self.dqn = (
            RLBuilder()
            .agent.build_agent(ActionResponse())
            .environment.build_env(DeCentralizedReward(), DeCentralizedState())
            .model_.build_model("decentralized", 4, 2)
            .build()
        )

        self.agent = agent
        self.coms = coms
        self.supported_services = supported_services
        self.services = []
        self.vehicles = kwargs.get("vehicles_list", [])
        self._supported_services_distinct = []
        self._capacity: float = 0.0
        # self.max_capacity = tower

        self._qvalue = 0.0
        self._current_capacity = self.set_max_capacity(self.__class__.__name__)
        self._max_capacity = self.set_max_capacity(self.__class__.__name__)
        # self._max_buffer_size = int(self._max_capacity / 30)
        # self._buffer_request = deque(maxlen=self._max_buffer_size)
        # print("int(self._max_capacity / 30) ", int(self._max_capacity / 30))
        # print("type : ", self.__class__.__name__)

    class BuildMaxCapacity:
        def calculate_max_capacity(
            self,
            num_antennas,
            channel_bandwidth,
            coding_rate,
            modulation_order,
            average_symbol_per_slot,
            num_slots_per_frame,
            num_frames_per_second,
        ):
            spectral_efficiency = modulation_order * coding_rate  # bits/symbol

            capacity_per_antenna = (
                channel_bandwidth
                * 1e6
                * spectral_efficiency
                * average_symbol_per_slot
                * num_slots_per_frame
                * num_frames_per_second
            ) / 1e6  # Mbps
            total_capacity = capacity_per_antenna * num_antennas
            real_total_capacity = total_capacity // 8 / 10
            # print(f"capacity is: {real_total_capacity} MBps")
            return real_total_capacity

        def randomized_tower_based_max_capacity(self, tower_type: dict):
            outlet = {}
            outlet_vals = []
            for k in tower_type:
                outlet[k] = np.random.choice(tower_type[k])
                outlet_vals = [*outlet.values()]
            real_total_capacity = self.calculate_max_capacity(*outlet_vals)
            return real_total_capacity

    @abstractmethod
    def calculate_coverage_area(self):
        pass

    @abstractmethod
    def calculate_downlink(self):
        pass

    @property
    def supported_services_distinct(self):
        return [self.supported_services, self._distinct]

    @property
    def qvalue(self):
        return self._qvalue

    @qvalue.setter
    def qvalue(self, value):
        self._qvalue = value

    @property
    def max_capacity(self):
        return self._max_capacity

    # @max_capacity.setter
    # def max_capacity(self, value):
    #     self._max_capacity = (
    #         self.BuildMaxCapacity().randomized_tower_based_max_capacity(value)
    #     )
    #     self._current_capacity = self._max_capacity

    def set_max_capacity(self, type):
        if type == "ThreeG":
            return 12500
        elif type == "FourG":
            return 25000
        elif type == "Wifi":
            return 3500
        else:
            return 50000

    @property
    def current_capacity(self):
        return self._current_capacity

    @current_capacity.setter
    def current_capacity(self, value):
        self._current_capacity = value

    # @property
    # def buffer_request(self):
    #     return self._buffer_request
    #
    # @buffer_request.setter
    # def buffer_request(self, value):
    #     self._buffer_request = value

    @property
    def max_buffer_size(self):
        return self._max_buffer_size

    @max_buffer_size.setter
    def max_buffer_size(self, value):
        self._max_buffer_size = value
