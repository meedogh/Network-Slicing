from Outlet.Cellular.Wifi import Wifi


class Drone:
    """
    outlet from type Air is the abstract class for UAV
    """

    def __init__(
        self,
        outlet: Wifi,
        position: tuple[float,float] = None,
        altitude: float = 100.0,
        aperture_radius: float = 0.05,
        fov: int = 90,  # degrees
    ) -> None:
        """

        Args:
            outlet: the wifi outlet
            position: x,y coordinates
            altitude: z coordinate
            radius: uav radius
        """
        self.position = outlet.position if position is None else position
        self.altitude = altitude
        self.aperture_radius = aperture_radius
        self.outlet = outlet
        self.fov = fov
        self.services = self.outlet.services = []

    def calculate_coverage_area(self) -> float:
        """Returns
        -------
        nothing , it is an abstract method
           The coverage area that the tower will response the requests in it."""
        pass
