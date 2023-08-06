import pytest

from Outlet.Cellular.Wifi import Wifi
from Outlet.Drone.uav import UAV
from Utils.config import outlet_types


@pytest.fixture
def wifi():
    return Wifi(
        outlet_types[str("3G")], 1, 1, [1, 1, 0], (1, 2), 10000, [1, 2], [10, 10, 10]
    )


@pytest.fixture
def uav(wifi):
    return UAV(wifi, (1.1, 1.3))


class TestAir:
    def test_default_values_assignment(self, uav):
        assert uav.altitude == 100.0

    def test_position_setting_None(self, uav):
        assert uav.position == (1.1, 1.3)

    def test_position_setting_value(self, wifi):
        uav = UAV(wifi)
        assert uav.position == (1, 2)
        assert uav.position == wifi.position

    def test_service_list_uav_same_as_service_list_wifi(self, uav, wifi):
        uav.services.append('dd')
        assert wifi.services[0] == 'dd'
