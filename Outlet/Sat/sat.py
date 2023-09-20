from Communications.IComs import Communications
from Outlet.IOutlet import Outlet
from collections import deque


class Satellite(Outlet):
    """
    outlet from type Satellite is the abstract class for UAV
    """

    def __init__(
            self, coms: Communications, supported_services, *args, **kwargs
    ):


        super().__init__(*args)
        self.coms = coms
        self.supported_services = supported_services
        self.services = []
        self.vehicles = kwargs.get("vehicles_list", [])
        self._supported_services_distinct = []
        self._max_capacity = 200000000
        self.rejected_requests_buffer = deque([])
        self._sum_of_costs_of_all_requests = 0

    @property
    def sum_of_costs_of_all_requests(self):
        return self._sum_of_costs_of_all_requests
    @sum_of_costs_of_all_requests.setter
    def sum_of_costs_of_all_requests(self,value ):
        self._sum_of_costs_of_all_requests=  value
    @property
    def supported_services_distinct(self):
        return [self.supported_services, self._distinct]

    @property
    def max_capacity(self):
        return self._max_capacity


    def calculate_coverage_area(self):
        """Returns
            -------
            nothing , it is an abstract method
               The coverage area that the tower will response the requests in it."""
        pass

    def calculate_downlink(self):
        """Returns
            -------
            nothing , it is an abstract method
               The downlink that the tower will use it for responsing the requests ."""
        pass
