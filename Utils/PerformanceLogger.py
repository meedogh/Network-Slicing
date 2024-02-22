import inspect
import warnings
from dataclasses import dataclass, field
from typing import List, Dict
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
class PerformanceLogger(metaclass=SingletonMeta):
    _services_type: str = ""

    _number_of_periods_until_now: int = -1

    _slice_num_dic : Dict[Service, int] = field(default_factory=dict)
 
    requested_services: List[Dict[Vehicle, Service]] = field(default_factory=list)

    handled_services: Dict[Outlet, Dict[Vehicle, Service]] = field(default_factory=dict)
    
    _sliced_requests: Dict[Service, List[Service]] = field(default_factory=dict)

    _served_slices: Dict[Service, bool] = field(default_factory=dict)

    _user_requests: Dict[Vehicle, Dict[str, deque[Service, bool:False,float]]] = field(default_factory=dict)

    _queue_requested_buffer: Dict[Outlet, int] = field(default_factory=dict)

    _number_of_requested_requests_buffer: Dict[Outlet, int] = field(default_factory=dict)

    # _accepted : int = 0
    # _served : int = 0
    # _time_out : int = 0
    _queue_power_for_requested_in_buffer: Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _queue_waiting_requests_in_buffer: Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _queue_requests_with_time_out_buffer: Dict[Outlet, Dict[Service, List[int]]] = field(default_factory=dict)

    _queue_time_out_from_simulation: Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _queue_from_wait_to_serve_over_simulation: Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _queue_wasted_req_buffer: Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _queue_ensured_buffer: Dict[Outlet, int] = field(default_factory=dict)

    _queue_requests_with_execution_time_buffer: Dict[Outlet, Dict[Service, List[int]]] = field(default_factory=dict)

    _outlet_services_power_allocation: Dict[Outlet, List[float]] = field(default_factory=dict)

    _generated_requests_over_simulation: int = field(default_factory=int)

    _served_requests_over_simulation: int = field(default_factory=int)

    _queue_request_failure_flags:Dict[Outlet, deque[Service, bool:False]] = field(default_factory=dict)

    _outlet_services_requested_number: Dict[Outlet, List[int]] = field(default_factory=dict)

    _outlet_services_requested_number_all_periods: Dict[Outlet, List[int]] = field(default_factory=dict)

    _outlet_services_ensured_number: Dict[Outlet, List[int]] = field(default_factory=dict)

    _request_costs: List[int] = field(default_factory=list)

    _power_costs: List[float] = field(default_factory=list)


    
    def initial_setting(self,outlet):
        self.set_outlet_services_power_allocation(outlet, [0, 0, 0])
        self.set_queue_requested_buffer(outlet, 0)
        self.set_queue_wasted_req_buffer(outlet, deque([]))
        self.set_queue_ensured_buffer(outlet, 0)
        self.set_queue_power_for_requested_in_buffer(outlet, deque([]))
        self.set_queue_waiting_requests_in_buffer(outlet, deque([]))
        self.set_queue_time_out_from_simulation(outlet, deque([]))
        self.set_queue_from_wait_to_serve_over_simulation(outlet, deque([]))
        self.set_queue_request_failure_flags(outlet, deque([]))
        self.set_outlet_services_requested_number_all_periods(outlet, [0, 0, 0])
        self.set_outlet_services_requested_number(outlet, [0, 0, 0])
        self.set_outlet_services_ensured_number(outlet, [0, 0, 0])
        self.set_number_of_requested_requests_buffer(outlet, 0)

        if outlet not in self.queue_requests_with_execution_time_buffer:
            self.queue_requests_with_execution_time_buffer[outlet] = dict()

        if outlet not in self.queue_requests_with_time_out_buffer:
            self.queue_requests_with_time_out_buffer[outlet] = dict()

    @property
    def slice_num_dic(self):
        return self._slice_num_dic
    
    @slice_num_dic.setter
    def slice_num_dic(self, data):
        id, value = data
        self._slice_num_dic[id] = value
    
    @property
    def sliced_requests(self):
        return self._sliced_requests

    @sliced_requests.setter
    def sliced_requests(self, data):
        id, value = data
        self._sliced_requests.setdefault(id, []).append(value)

    @property
    def served_slices(self):
        return self._served_slices

    @served_slices.setter
    def served_slices(self, data):
        id, value = data
        self._served_slices.setdefault(id, []).append(value)


    @property
    def accepted(self):
        return self._accepted

    @accepted.setter
    def accepted(self,value):
        self._accepted =  value

    @property
    def served(self):
        return self._served
    
    @served.setter
    def served(self,value ):
        self._served =  value

    @property
    def time_out(self):
        return self._time_out
    @time_out.setter
    def time_out(self,value ):
        self._time_out = value
    @property
    def queue_requested_buffer(self):
        return self._queue_requested_buffer

    def set_queue_requested_buffer(self, outlet, value):
        if outlet not in self._queue_requested_buffer:
            self._queue_requested_buffer[outlet] = {}
        self._queue_requested_buffer[outlet] = value


    @property
    def number_of_requested_requests_buffer(self):
        return self._number_of_requested_requests_buffer
    
    def set_number_of_requested_requests_buffer(self,outlet,value):
        if outlet not in self._number_of_requested_requests_buffer :
            self._number_of_requested_requests_buffer[outlet] = {}
        self._number_of_requested_requests_buffer[outlet] = value

    @property
    def queue_request_failure_flags(self):
        return self._queue_request_failure_flags

    def set_queue_request_failure_flags(self, outlet, value):
        if outlet not in self._queue_request_failure_flags:
            self._queue_request_failure_flags[outlet] = {}
        self._queue_request_failure_flags[outlet] = value

    @property
    def generated_requests_over_simulation(self):
        return self._generated_requests_over_simulation

    @generated_requests_over_simulation.setter
    def generated_requests_over_simulation(self,value):
        self._generated_requests_over_simulation = value

    @property
    def served_requests_over_simulation(self):
        return self._served_requests_over_simulation

    @served_requests_over_simulation.setter
    def served_requests_over_simulation(self,value):
        self._served_requests_over_simulation = value
    
    @property
    def queue_wasted_req_buffer(self):
        return self._queue_wasted_req_buffer

    def set_queue_wasted_req_buffer(self, outlet, value):
        if outlet not in self._queue_wasted_req_buffer:
            self._queue_wasted_req_buffer[outlet] = {}
        self._queue_wasted_req_buffer[outlet] = value

    @property
    def queue_requests_with_time_out_buffer(self):
        return self._queue_requests_with_time_out_buffer

    def set_queue_requests_with_time_out_buffer(self, outlet, service, value):
        if service not in self._queue_requests_with_time_out_buffer:
            self._queue_requests_with_time_out_buffer[outlet] = {}
        new_value = {service: value}
        self._queue_requests_with_time_out_buffer[outlet].update(new_value)

    # _queue_from_wait_to_serve_over_simulation

    @property
    def queue_from_wait_to_serve_over_simulation(self):
        return self._queue_from_wait_to_serve_over_simulation

    def set_queue_from_wait_to_serve_over_simulation(self, outlet, value):
        if outlet not in self._queue_from_wait_to_serve_over_simulation:
            self._queue_from_wait_to_serve_over_simulation[outlet] = {}
        self._queue_from_wait_to_serve_over_simulation[outlet] = value

    @property
    def queue_time_out_from_simulation(self):
        return self._queue_time_out_from_simulation

    def set_queue_time_out_from_simulation(self, outlet, value):
        if outlet not in self._queue_time_out_from_simulation:
            self._queue_time_out_from_simulation[outlet] = {}
        self._queue_time_out_from_simulation[outlet] = value

    @property
    def queue_requests_with_execution_time_buffer(self):
        return self._queue_requests_with_execution_time_buffer

    def set_queue_requests_with_execution_time_buffer(self, outlet, service, value):
        if service not in self._queue_requests_with_execution_time_buffer:
            self._queue_requests_with_execution_time_buffer[outlet] = {}
        new_value = {service: value}
        self._queue_requests_with_execution_time_buffer[outlet].update(new_value)

    @property
    def queue_waiting_requests_in_buffer(self):
        return self._queue_waiting_requests_in_buffer

    def set_queue_waiting_requests_in_buffer(self, outlet, value):
        if outlet not in self._queue_waiting_requests_in_buffer:
            self._queue_waiting_requests_in_buffer[outlet] = {}
        self._queue_waiting_requests_in_buffer[outlet] = value

    @property
    def queue_power_for_requested_in_buffer(self):
        return self._queue_power_for_requested_in_buffer

    def set_queue_power_for_requested_in_buffer(self, outlet, value):
        if outlet not in self._queue_power_for_requested_in_buffer:
            self._queue_power_for_requested_in_buffer[outlet] = {}
        self._queue_power_for_requested_in_buffer[outlet] = value

    @property
    def queue_ensured_buffer(self):
        return self._queue_ensured_buffer

    def set_queue_ensured_buffer(self, outlet, value):
        if outlet not in self._queue_ensured_buffer:
            self._queue_ensured_buffer[outlet] = {}
        self._queue_ensured_buffer[outlet] = value

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
    def user_requests(self):
        return self._user_requests

    def set_user_requests(self, outlet, car, service, boolValue):
        if car not in self._user_requests:
            self._user_requests[car] = {}

        outlet_type = outlet.__class__.__name__

        if outlet_type not in self._user_requests[car]:
            self._user_requests[car][outlet_type] = deque([])

        if [service, boolValue, 0.0] not in self._user_requests[car][outlet_type]:
            self._user_requests[car][outlet_type].append([service, boolValue, 0.0])



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
            self._queue_requested_buffer[key] = -1
        for key in self._queue_ensured_buffer:
            self._queue_ensured_buffer[key] = -1
        for key in self._queue_power_for_requested_in_buffer:
            self._queue_power_for_requested_in_buffer[key] = deque([])
        for key in self._queue_waiting_requests_in_buffer:
            self._queue_waiting_requests_in_buffer[key] = deque([])
        for key in self._queue_requests_with_execution_time_buffer:
            self._queue_requests_with_execution_time_buffer[key] = dict()
        for key in self._queue_requests_with_time_out_buffer:
            self._queue_requests_with_time_out_buffer[key] = dict()
        for key in self._outlet_services_requested_number:
            self._outlet_services_requested_number[key] = [0, 0, 0]
        for key in self._outlet_services_ensured_number:
            self._outlet_services_ensured_number[key] = [0, 0, 0]
        for key in self._queue_from_wait_to_serve_over_simulation:
            self._queue_from_wait_to_serve_over_simulation[key] = deque([])
        for key in self._queue_time_out_from_simulation:
            self._queue_time_out_from_simulation[key] = deque([])
        self._generated_requests_over_simulation = -1
        self._served_requests_over_simulation = -1
        for key in self._number_of_requested_requests_buffer:
            self._number_of_requested_requests_buffer[key]= -1
