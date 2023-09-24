import copy
# import rx
# import rx.operators as ops
import numpy as np
from RL.RLEnvironment.State.State import State


class DeCentralizedState(State):
    allocated_power: [float]
    _services_ensured: int
    _services_requested: int
    _tower_capacity = 0.0
    _max_tower_capacity = 0.0
    _state_value_decentralize = [0.0] * 4
    _next_state_decentralize = [0.0] * 4

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = DeCentralizedState.state_shape(self.num_services, self.grid_cell)
        self._allocated_power = np.zeros(3)
        self._supported_services = copy.deepcopy(self.allocated_power)
        self._services_ensured = 0
        self._services_requested = 0
        self._tower_capacity = 0.0
        self._index_service = 0
        self._power_of_requests = 0
        self._action_value = 0
        self._number_requested_in_period = np.zeros(self.num_services)
        self._number_ensured_in_period = np.zeros(self.num_services)
        self._ratio_of_occupancy = 0
        self._waiting_buffer_len = 0
        self._remaining_time_out = 0
        self._timed_out_length = 0
        self._wasting_buffer_length = 0
        self._from_waiting_to_serv_length = 0
        self._time_out_requests_over_simulation = 0
        self._from_wait_to_serve_over_simulation = 0
        self._delay_time = 0
        self._time_out_flag = 0
        self.number_of_timed_out_requests_from_algorithm = 0
        self._tower_capacity_before_time_out_step_service = 0

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

    @property
    def tower_capacity_before_time_out_step_service(self):
        return self._tower_capacity_before_time_out_step_service
    @tower_capacity_before_time_out_step_service.setter
    def tower_capacity_before_time_out_step_service(self,value):
        self._tower_capacity_before_time_out_step_service = value

    @property
    def time_out_flag(self):
        return self._time_out_flag

    @time_out_flag.setter
    def time_out_flag(self, value):
        self._time_out_flag = value

    @property
    def delay_time(self):
        return self._delay_time

    @delay_time.setter
    def delay_time(self, value):
        self._delay_time = value

    @property
    def from_wait_to_serve_over_simulation(self):
        return self._from_wait_to_serve_over_simulation

    @from_wait_to_serve_over_simulation.setter
    def from_wait_to_serve_over_simulation(self, value):
        self._from_wait_to_serve_over_simulation = value

    @property
    def time_out_requests_over_simulation(self):
        return self._time_out_requests_over_simulation

    @time_out_requests_over_simulation.setter
    def time_out_requests_over_simulation(self, value):
        self._time_out_requests_over_simulation = value

    @property
    def wasting_buffer_length(self):
        return self._wasting_buffer_length

    @wasting_buffer_length.setter
    def wasting_buffer_length(self, value):
        self._wasting_buffer_length = value

    @property
    def from_waiting_to_serv_length(self):
        return self._from_waiting_to_serv_length

    @from_waiting_to_serv_length.setter
    def from_waiting_to_serv_length(self, value):
        self._from_waiting_to_serv_length = value

    @property
    def timed_out_length(self):
        return self._timed_out_length

    @timed_out_length.setter
    def timed_out_length(self, value):
        self._timed_out_length = value

    @property
    def waiting_buffer_len(self):
        return self._waiting_buffer_len

    @waiting_buffer_len.setter
    def waiting_buffer_len(self, value):
        self._waiting_buffer_len = value

    @property
    def remaining_time_out(self):
        return self._remaining_time_out

    @remaining_time_out.setter
    def remaining_time_out(self, value):
        self._remaining_time_out = value

    @property
    def ratio_of_occupancy(self):
        return self._ratio_of_occupancy

    @ratio_of_occupancy.setter
    def ratio_of_occupancy(self, value):
        self._ratio_of_occupancy = value

    @property
    def power_of_requests(self):
        return self._power_of_requests

    @power_of_requests.setter
    def power_of_requests(self, value):
        self._power_of_requests = value

    @property
    def number_requested_in_period(self):
        return self._number_requested_in_period

    @number_requested_in_period.setter
    def number_requested_in_period(self, value):
        self._number_requested_in_period = value

    @property
    def number_ensured_in_period(self):
        return self._number_ensured_in_period

    @number_ensured_in_period.setter
    def number_ensured_in_period(self, value):
        self._number_ensured_in_period = value

    @property
    def index_service(self):
        return self._index_service

    @index_service.setter
    def index_service(self, value):
        self._index_service = value

    @property
    def action_value(self):
        return self._action_value

    @action_value.setter
    def action_value(self, value):
        self._action_value = value

    @property
    def state_value_decentralize(self):
        return self._state_value_decentralize

    @state_value_decentralize.setter
    def state_value_decentralize(self, val):
        self._state_value_decentralize = val

    @property
    def next_state_decentralize(self):
        return self._next_state_decentralize

    @next_state_decentralize.setter
    def next_state_decentralize(self, val):
        self._next_state_decentralize = val

    @property
    def tower_capacity(self):
        return self._tower_capacity

    @tower_capacity.setter
    def tower_capacity(self, value):
        self._tower_capacity = value

    @property
    def max_tower_capacity(self):
        return self._max_tower_capacity

    @max_tower_capacity.setter
    def max_tower_capacity(self, value):
        self._max_tower_capacity = value

    @property
    def services_requested(self):
        return self._services_requested

    @services_requested.setter
    def services_requested(self, value):
        self._services_requested = value

    @property
    def services_ensured(self):
        return self._services_ensured

    @services_ensured.setter
    def services_ensured(self, value):
        self._services_ensured = value

    @property
    def allocated_power(self):
        return self._allocated_power

    @property
    def supported_services(self):
        return self._supported_services

    @allocated_power.setter
    def allocated_power(self, power_array):
        self._allocated_power = power_array

    @supported_services.setter
    def supported_services(self, supported_array):
        self._supported_services = supported_array

    def resetsate(self):
        self.state_value_decentralize = [0.0] * 4
        self.power_of_requests = 0
        self.tower_capacity = self.max_tower_capacity
        self.remaining_time_out = 0
        self.waiting_buffer_len = 0
        self.timed_out_length = 0
        self.from_waiting_to_serv_length = 0
        self.services_ensured = 0
        self.services_requested = 0
        self._time_out_requests_over_simulation = 0
        self._from_wait_to_serve_over_simulation = 0
        self._delay_time = 0
        self.number_of_timed_out_requests_from_algorithm = 0
    def calculate_state(self, outlet_max_len):
        final_state = []
        # final_state.append((self.max_tower_capacity / self.max_tower_capacity) * 100)
        final_state.append(self.remaining_time_out)
        final_state.append(round(((self._tower_capacity / self.max_tower_capacity) * 100), 2))
        final_state.append(round(((self.power_of_requests / self.max_tower_capacity) * 100), 2))
        final_state.append(round(((self.waiting_buffer_len / outlet_max_len) * 100), 2))
        # final_state.append(round(((self._tower_capacity_before_time_out_step_service / self.max_tower_capacity)*100),2))

        # final_state.append(self._time_out_flag)

        if len(final_state) == 0:
            final_state = [0.0] * 4
        return final_state
