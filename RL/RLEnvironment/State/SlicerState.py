

from RL.RLEnvironment.State.State import State
class SlicerState(State):
    _state_value_decentralize = [0.0]*9
    _next_state_decentralize = [0.0]*9
    def __init__(self):
        super().__init__()
        self._available_capacity_wifi = 0
        self._available_capacity_3G = 0
        self._available_capacity_4G = 0
        self._available_capacity_5G = 0
        self._buffer_occupancy_wifi = 0
        self._buffer_occupancy_3G = 0
        self._buffer_occupancy_4G = 0
        self._buffer_occupancy_5G = 0
        self._request_power_allocation = 0

    @property
    def available_capacity_wifi(self):
        return self._available_capacity_wifi
    @available_capacity_wifi.setter
    def available_capacity_wifi(self,capacity):
        self._available_capacity_wifi = capacity

    @property
    def available_capacity_3G(self):
        return self._available_capacity_3G

    @available_capacity_3G.setter
    def available_capacity_3G(self, capacity):
        self._available_capacity_3G = capacity

    @property
    def available_capacity_4G(self):
        return self._available_capacity_4G

    @available_capacity_4G.setter
    def available_capacity_4G(self, capacity):
        self._available_capacity_4G = capacity

    @property
    def available_capacity_5G(self):
        return self._available_capacity_5G

    @available_capacity_5G.setter
    def available_capacity_5G(self, capacity):
        self._available_capacity_5G = capacity

    @property
    def buffer_occupancy_wifi(self):
        return self._buffer_occupancy_wifi

    @buffer_occupancy_wifi.setter
    def buffer_occupancy_wifi(self,occupancy):
        self._buffer_occupancy_wifi  =  occupancy

    @property
    def buffer_occupancy_3G(self):
        return self._buffer_occupancy_3G

    @buffer_occupancy_3G.setter
    def buffer_occupancy_3G(self, occupancy):
        self._buffer_occupancy_3G = occupancy

    @property
    def buffer_occupancy_4G(self):
        return self._buffer_occupancy_4G

    @buffer_occupancy_4G.setter
    def buffer_occupancy_4G(self, occupancy):
        self._buffer_occupancy_4G = occupancy

    @property
    def buffer_occupancy_5G(self):
        return self._buffer_occupancy_5G

    @buffer_occupancy_5G.setter
    def buffer_occupancy_5G(self, occupancy):
        self._buffer_occupancy_5G = occupancy

    @property
    def state_value_decentralize(self):
        return self._state_value_decentralize

    @state_value_decentralize.setter
    def state_value_decentralize(self,state_value):
        self._state_value_decentralize = state_value

    @property
    def next_state_decentralize(self):
        return self._next_state_decentralize
    @next_state_decentralize.setter
    def next_state_decentralize(self,next_state_value):
        self._next_state_decentralize = next_state_value
    def calculate_state(self):
        pass
    def resetstate(self):
        pass







