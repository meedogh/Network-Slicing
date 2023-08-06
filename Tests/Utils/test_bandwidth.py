import pytest

from Utils.Bandwidth import Bandwidth


@pytest.fixture
def bandwidth():
    return Bandwidth(3, 10)


def test_set_bandwidth_and_criticality(bandwidth):
    assert bandwidth.bandwidth_demand == 3 and bandwidth.criticality == 10


def test_set_and_return_allocated(bandwidth):
    # Arrange
    total_bandwidth = bandwidth.bandwidth_demand * 10
    change_in_bandwidth = bandwidth.criticality * total_bandwidth * 0.03
    total_bandwidth = total_bandwidth + change_in_bandwidth

    assert bandwidth.allocated == total_bandwidth
