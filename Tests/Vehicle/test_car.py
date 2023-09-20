from unittest.mock import Mock

import pytest

from vehicle.car import Car


@pytest.fixture
def car():
    return Car(2, 10, 3)


def test_car_inherits_attributes_from_interface_vehicle(car):
    assert car.x == 10 and car.y == 3


def test_car_attach(car):
    car.attach("gg")
    assert len(car.observers) == 1


def test_car_detach(car):
    car.attach('gg')
    car.detach('gg')
    assert len(car.observers) == 0


def test_car_detach_of_a_variable_not_in_list(car):
    with pytest.raises(ValueError):
        car.detach('ss')


def test_changin_car_coordinantes(car):
    car.set_state(20, 10)
    assert car.x == 20 and car.y == 10


def test_car_notifying_subscribed_observers(car):
    observer = Mock()

    car.attach(observer)
    print(car.observers)
    car.notify()

    observer.update.assert_called_once_with(car)
