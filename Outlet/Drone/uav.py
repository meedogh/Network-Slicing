from Outlet.Drone.drone import Drone
import math


class UAV(Drone):
    def calculate_coverage_area(self):
        distance_to_object = self.altitude / math.tan(math.radians(self.fov / 2))
        radius = (self.altitude * self.aperture_radius) / distance_to_object

        area = math.pi * radius ** 2

        return area

