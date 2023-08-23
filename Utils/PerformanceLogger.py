import inspect
import warnings
from dataclasses import dataclass, field
from typing import List, Dict
from RL.Agent.Agent import Agent
from Vehicle.IVehicle import Vehicle
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
class PerformanceLogger(metaclass=SingletonMeta):

    _services_type: str = ""

    _number_of_periods_until_now: int = -1

    requested_services: List[Dict[Vehicle, Service]] = field(default_factory=list)

    handled_services: Dict[Outlet, Dict[Vehicle, Service]] = field(default_factory=dict)

    _queue_requested_buffer: Dict[Outlet, deque[int]] =  field(default_factory=dict)

    _queue_power_for_requested_in_buffer: Dict[Outlet, deque[Service,bool:False]] = field(default_factory=dict)

    _queue_waiting_requests_in_buffer : Dict[Outlet, deque[Service,bool:False]] = field(default_factory=dict)

    _queue_time_out_buffer: Dict[Outlet,Dict[Service, List[int]]] = field(default_factory=dict)

    _queue_wasted_req_buffer: Dict[Outlet,Dict[Service, List[int]]] = field(default_factory=dict)



    _queue_ensured_buffer: Dict[Outlet, deque[int]] = field(default_factory=dict)

    _queue_provisioning_time_buffer: Dict[Outlet,Dict[Service, List[int]]] = field(default_factory=dict)

    _outlet_services_power_allocation: Dict[Outlet, List[float]] = field(default_factory=dict)

    _outlet_services_power_allocation_10_TimeStep: Dict[Outlet, List[float]] = field(default_factory=dict)

    _outlet_services_requested_number: Dict[Outlet, List[int]] = field(default_factory=dict)

    _outlet_services_requested_number_all_periods: Dict[Outlet, List[int]] = field(default_factory=dict)

    _outlet_services_ensured_number: Dict[Outlet, List[int]] = field(default_factory=dict)

    _request_costs: List[int] = field(default_factory=list)

    _power_costs: List[float] = field(default_factory=list)

    @property
    def queue_requested_buffer(self):
        return self._queue_requested_buffer

    def set_queue_requested_buffer(self, outlet,value):
        if outlet not in self._queue_requested_buffer:
            self._queue_requested_buffer[outlet] = {}
        self._queue_requested_buffer[outlet] = value

    @property
    def queue_wasted_req_buffer(self):
        return self._queue_wasted_req_buffer

    def set_queue_wasted_req_buffer(self, outlet, service, value):
        if service not in self._queue_wasted_req_buffer:
            self._queue_wasted_req_buffer[outlet] = {}
        new_value = {service: value}
        self._queue_wasted_req_buffer[outlet].update(new_value)
    @property
    def queue_time_out_buffer(self):
        return self._queue_time_out_buffer

    def set_queue_time_out_buffer(self, outlet, service, value):
        if service not in self._queue_time_out_buffer:
            self._queue_time_out_buffer[outlet] = {}
        new_value = {service: value}
        self._queue_time_out_buffer[outlet].update(new_value)

    @property
    def queue_provisioning_time_buffer(self):
        return self._queue_provisioning_time_buffer

    def set_queue_provisioning_time_buffer(self, outlet,service, value):
        if service not in self._queue_provisioning_time_buffer:
            self._queue_provisioning_time_buffer[outlet] = {}
        new_value = {service: value}
        self._queue_provisioning_time_buffer[outlet].update(new_value)


    @property
    def queue_waiting_requests_in_buffer(self):
        return self._queue_waiting_requests_in_buffer

    def set_queue_waiting_requests_in_buffer(self, outlet,value):
        max_len = 0
        if outlet.__class__.__name__ == "wifi":
            max_len= 45
        if outlet.__class__.__name__ == "ThreeG":
            max_len= 125
        if outlet.__class__.__name__ == "FourG":
            max_len= 250
        if outlet.__class__.__name__ == "FiveG":
            max_len= 500
        if outlet not in self._queue_waiting_requests_in_buffer:
            self._queue_waiting_requests_in_buffer[outlet] = {}
        self._queue_waiting_requests_in_buffer[outlet]=value

    @property
    def queue_power_for_requested_in_buffer(self):
        return self._queue_power_for_requested_in_buffer

    def set_queue_power_for_requested_in_buffer(self, outlet,value):
        if outlet not in self._queue_power_for_requested_in_buffer:
            self._queue_power_for_requested_in_buffer[outlet] = {}
        self._queue_power_for_requested_in_buffer[outlet]=value


    @property
    def queue_ensured_buffer(self):
        return self._queue_ensured_buffer

    def set_queue_ensured_buffer(self, outlet, value):
        if outlet not in self._queue_ensured_buffer:
            self._queue_ensured_buffer[outlet] = {}
        self._queue_ensured_buffer[outlet] = value

    @property
    def gridcell_utility(self):
        return self._gridcell_utility

    def set_gridcell_utility(self, outlet, utility):
        if outlet not in self._gridcell_utility:
            self._gridcell_utility[outlet] = {}
        self._gridcell_utility[outlet] = utility



    @property
    def service_power_allocate(self):
        return self._service_power_allocate

    def set_service_power_allocate(self, outlet, cost):
        if outlet not in self._service_power_allocate:
            self._service_power_allocate[outlet] = {}
        self._service_power_allocate[outlet] = cost

    @property
    def outlet_services_power_allocation_10_TimeStep(self):
        return self._outlet_services_power_allocation_10_TimeStep

    def set_outlet_services_power_allocation_10_TimeStep(self, outlet, cost):
        if outlet not in self._outlet_services_power_allocation_10_TimeStep:
            self._outlet_services_power_allocation_10_TimeStep[outlet] = {}
        self._outlet_services_power_allocation_10_TimeStep[outlet] = cost



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
            self._outlet_services_power_allocation[outlet]= {}
        self._outlet_services_power_allocation[outlet] = service




    @property
    def service_requested(self):
        return self.requested_services

    @service_requested.setter
    def service_requested(self, value):
        self.requested_services.append(value)

    @property
    def service_handled(self):
        return self.handled_services

    def set_service_handled(self, outlet, car, service):
        if outlet not in self.handled_services:
            self.handled_services[outlet] = {}
        new_value = {car: service}
        self.handled_services[outlet].update(new_value)

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
        for key in self._queue_requested_buffer:
            self._queue_requested_buffer[key] = deque([])
        for key in self._queue_ensured_buffer:
            self._queue_ensured_buffer[key] = deque([])
        for key in self._queue_power_for_requested_in_buffer:
            self._queue_power_for_requested_in_buffer[key] = deque([])
        for key in self._queue_waiting_requests_in_buffer:
            self._queue_waiting_requests_in_buffer[key] = deque([])
        for key in self._queue_provisioning_time_buffer:
            self._queue_provisioning_time_buffer[key] = dict()
        for key in self._queue_time_out_buffer:
            self._queue_time_out_buffer[key] = dict()
        for key in self._outlet_services_requested_number:
            self._outlet_services_requested_number[key] = [0,0,0]
        for key in self._outlet_services_ensured_number:
            self._outlet_services_ensured_number[key] = [0,0,0]

        # for key in self._outlet_services_requested_number:
        #     self._outlet_services_requested_number[key] = [0, 0, 0]
        # for key in self._outlet_services_ensured_number:
        #     self._outlet_services_ensured_number[key] = [0, 0, 0]
        # for key in self._outlet_services_power_allocation:
        #     self._outlet_services_power_allocation[key] = [0, 0, 0]
        # for key in self.handled_services:
        #     self.handled_services[key] = {}
