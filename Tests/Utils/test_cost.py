from unittest.mock import Mock

import pytest
from Utils.Cost import Cost, RequestCost, TowerCost
from Utils.Bandwidth import Bandwidth


@pytest.fixture
def bandwidth():
    return Bandwidth(2, 3)


@pytest.fixture
def cost(bandwidth):
    return Cost(bandwidth, 2)


@pytest.fixture
def request_cost(bandwidth):
    return RequestCost(bandwidth, 2)


def test_set_bandwidth_and_reality(cost, bandwidth):
    assert cost.realtime == 2 and cost.bit_rate == bandwidth.allocated and cost._cost == 0


def test_setter_cost(cost):
    cost.cost_setter(cost.realtime)
    assert cost.cost == 21.8


# def test_request_cost(request_cost):
#     request_cost.cost_setter(request_cost.realtime)
#     assert request_cost.cost == (21.8 * 0.15)


# def test_request_string(request_cost):
#     request_cost.cost_setter(request_cost.realtime)
#     assert request_cost.__str__() == f'Request Fee: {21.8 * 0.15}'
