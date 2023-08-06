from Communications.IComs import Communications
from Outlet.IOutlet import Outlet


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
