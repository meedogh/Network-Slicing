import inspect
import warnings
from dataclasses import dataclass, field
from typing import List, Dict
from RL.Agent.Agent import Agent
from vehicle.IVehicle import Vehicle
from Service.IService import Service
from Outlet.IOutlet import Outlet
from collections import deque


class SingletonMeta(type):
    """
    Metaclass that ensures only one instance of a class is created.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class PerformanceLoggerFifo(metaclass=SingletonMeta):
    _services_type: str = ""

    _number_of_periods_until_now: int = -1

    _queue_requested_buffer_for_fifo: Dict[Outlet, deque[int]] = field(default_factory=dict)

    _queue_power_for_requested_in_buffer_for_fifo: Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _queue_waiting_requests_in_buffer_for_fifo: Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _queue_requests_with_time_out_buffer_for_fifo: Dict[Outlet, Dict[Service, List[int]]] = field(default_factory=dict)

    _queue_time_out_from_simulation_for_fifo: Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _queue_from_wait_to_serve_over_simulation_for_fifo: Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _queue_wasted_req_buffer_for_fifo: Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _queue_ensured_buffer_for_fifo: Dict[Outlet, deque[int]] = field(default_factory=dict)

    _queue_requests_with_execution_time_buffer_for_fifo: Dict[Outlet, Dict[Service, List[int]]] = field(default_factory=dict)

    _outlet_services_power_allocation: Dict[Outlet, List[float]] = field(default_factory=dict)

    _generated_requests_over_simulation_for_fifo: deque[int] = field(default_factory=deque)

    _outlet_services_requested_number: Dict[Outlet, List[int]] = field(default_factory=dict)

    _outlet_services_requested_number_all_periods: Dict[Outlet, List[int]] = field(default_factory=dict)

    _outlet_services_ensured_number: Dict[Outlet, List[int]] = field(default_factory=dict)

    _request_costs: List[int] = field(default_factory=list)

    _power_costs: List[float] = field(default_factory=list)

    @property
    def queue_requested_buffer(self):
        return self._queue_requested_buffer_for_fifo

    def set_queue_requested_buffer_for_fifo(self, outlet, value):
        if outlet not in self._queue_requested_buffer_for_fifo:
            self._queue_requested_buffer_for_fifo[outlet] = {}
        self._queue_requested_buffer_for_fifo[outlet] = value

    @property
    def generated_requests_over_simulation(self):
        return self._generated_requests_over_simulation_for_fifo

    @property
    def queue_wasted_req_buffer(self):
        return self._queue_wasted_req_buffer_for_fifo

    def set_queue_wasted_req_buffer_for_fifo(self, outlet, value):
        if outlet not in self._queue_wasted_req_buffer_for_fifo:
            self._queue_wasted_req_buffer_for_fifo[outlet] = {}
        self._queue_wasted_req_buffer_for_fifo[outlet] = value

    @property
    def queue_requests_with_time_out_buffer(self):
        return self._queue_requests_with_time_out_buffer_for_fifo

    def set_queue_requests_with_time_out_buffer_for_fifo(self, outlet, service, value):
        if service not in self._queue_requests_with_time_out_buffer_for_fifo:
            self._queue_requests_with_time_out_buffer_for_fifo[outlet] = {}
        new_value = {service: value}
        self._queue_requests_with_time_out_buffer_for_fifo[outlet].update(new_value)

    # _queue_from_wait_to_serve_over_simulation

    @property
    def queue_from_wait_to_serve_over_simulation(self):
        return self._queue_from_wait_to_serve_over_simulation_for_fifo

    def set_queue_from_wait_to_serve_over_simulation_for_fifo(self, outlet, value):
        if outlet not in self._queue_from_wait_to_serve_over_simulation_for_fifo:
            self._queue_from_wait_to_serve_over_simulation_for_fifo[outlet] = {}
        self._queue_from_wait_to_serve_over_simulation_for_fifo[outlet] = value

    @property
    def queue_time_out_from_simulation(self):
        return self._queue_time_out_from_simulation_for_fifo

    def set_queue_time_out_from_simulation_for_fifo(self, outlet, value):
        if outlet not in self._queue_time_out_from_simulation_for_fifo:
            self._queue_time_out_from_simulation_for_fifo[outlet] = {}
        self._queue_time_out_from_simulation_for_fifo[outlet] = value

    @property
    def queue_requests_with_execution_time_buffer(self):
        return self._queue_requests_with_execution_time_buffer_for_fifo

    def set_queue_requests_with_execution_time_buffer_for_fifo(self, outlet, service, value):
        if service not in self._queue_requests_with_execution_time_buffer_for_fifo:
            self._queue_requests_with_execution_time_buffer_for_fifo[outlet] = {}
        new_value = {service: value}
        self._queue_requests_with_execution_time_buffer_for_fifo[outlet].update(new_value)

    @property
    def queue_waiting_requests_in_buffer(self):
        return self._queue_waiting_requests_in_buffer_for_fifo

    def set_queue_waiting_requests_in_buffer_for_fifo(self, outlet, value):
        if outlet not in self._queue_waiting_requests_in_buffer_for_fifo:
            self._queue_waiting_requests_in_buffer_for_fifo[outlet] = {}
        self._queue_waiting_requests_in_buffer_for_fifo[outlet] = value

    @property
    def queue_power_for_requested_in_buffer(self):
        return self._queue_power_for_requested_in_buffer_for_fifo

    def set_queue_power_for_requested_in_buffer_for_fifo(self, outlet, value):
        if outlet not in self._queue_power_for_requested_in_buffer_for_fifo:
            self._queue_power_for_requested_in_buffer_for_fifo[outlet] = {}
        self._queue_power_for_requested_in_buffer_for_fifo[outlet] = value

    @property
    def queue_ensured_buffer(self):
        return self._queue_ensured_buffer_for_fifo

    def set_queue_ensured_buffer_for_fifo(self, outlet, value):
        if outlet not in self._queue_ensured_buffer_for_fifo:
            self._queue_ensured_buffer_for_fifo[outlet] = {}
        self._queue_ensured_buffer_for_fifo[outlet] = value

    @property
    def outlet_services_ensured_number(self):
        return self._outlet_services_ensured_number

    def set_outlet_services_ensured_number(self, outlet, num):
        if outlet not in self._outlet_services_ensured_number:
            self._outlet_services_ensured_number[outlet] = {}
        self._outlet_services_ensured_number[outlet] = num

    @property
    def outlet_services_requested_number(self):
        return self._outlet_services_requested_number

    def set_outlet_services_requested_number(self, outlet, num):
        if outlet not in self._outlet_services_requested_number:
            self._outlet_services_requested_number[outlet] = {}
        self._outlet_services_requested_number[outlet] = num

    @property
    def outlet_services_requested_number_all_periods(self):
        return self._outlet_services_requested_number_all_periods

    def set_outlet_services_requested_number_all_periods(self, outlet, num):
        if outlet not in self._outlet_services_requested_number_all_periods:
            self._outlet_services_requested_number_all_periods[outlet] = {}
        self._outlet_services_requested_number_all_periods[outlet] = num

    @property
    def outlet_services_power_allocation(self):
        return self._outlet_services_power_allocation

    def set_outlet_services_power_allocation(self, outlet, service):
        if outlet not in self._outlet_services_power_allocation:
            self._outlet_services_power_allocation[outlet] = {}
        self._outlet_services_power_allocation[outlet] = service


    @property
    def request_costs(self):
        return self._request_costs

    @request_costs.setter
    def request_costs(self, value):
        print("inside request cost setter  :  >>>>> ", value)
        self._request_costs.append(value)

    @property
    def power_costs(self) -> List[float]:
        return self._power_costs

    @power_costs.setter
    def power_costs(self, value: List[float] | int) -> None:
        if not isinstance(value, List):
            self._power_costs.append(value)
            current_frame = inspect.currentframe()
            lineno = current_frame.f_back.f_lineno
            warnings.warn_explicit(
                "power cost should be appended and not set",
                category=UserWarning,
                filename=__file__,
                lineno=lineno,
            )
        else:
            self._power_costs.extend(value)

    def reset_state_decentralize_requirement(self):
        for key in self._queue_requested_buffer_for_fifo:
            self._queue_requested_buffer_for_fifo[key] = deque([])
        for key in self._queue_ensured_buffer_for_fifo:
            self._queue_ensured_buffer_for_fifo[key] = deque([])
        for key in self._queue_power_for_requested_in_buffer_for_fifo:
            self._queue_power_for_requested_in_buffer_for_fifo[key] = deque([])
        for key in self._queue_waiting_requests_in_buffer_for_fifo:
            self._queue_waiting_requests_in_buffer_for_fifo[key] = deque([])
        for key in self._queue_requests_with_execution_time_buffer_for_fifo:
            self._queue_requests_with_execution_time_buffer_for_fifo[key] = dict()
        for key in self._queue_requests_with_time_out_buffer_for_fifo:
            self._queue_requests_with_time_out_buffer_for_fifo[key] = dict()
        for key in self._outlet_services_requested_number:
            self._outlet_services_requested_number[key] = [0, 0, 0]
        for key in self._outlet_services_ensured_number:
            self._outlet_services_ensured_number[key] = [0, 0, 0]
        for key in self._queue_from_wait_to_serve_over_simulation_for_fifo:
            self._queue_from_wait_to_serve_over_simulation_for_fifo[key] = deque([])
        for key in self._queue_time_out_from_simulation_for_fifo:
            self._queue_time_out_from_simulation_for_fifo[key] = deque([])
        self._generated_requests_over_simulation_for_fifo = deque()
