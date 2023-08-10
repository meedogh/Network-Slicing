import math

from RL.RLEnvironment.Reward.Reward import Reward
import numpy as np


class DeCentralizedReward(Reward):
    _services_ensured: int
    _services_requested: int



    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = DeCentralizedReward.state_shape(self.num_services, self.grid_cell)
        self._services_ensured = 0
        self._services_requested = 0
        self._prev_utility = 0
        self.reward_value = 0
        self._dx_t = 0.0
        self._dx_t_prev = 0.0
        self._coeff = 0
        self._period_reward_decentralize = []
        self._episode_reward_decentralize = []
        self._throughput_weight = 1
        self._throughput_derivation_weight = 1
        self._cost_derivation_weight = 0.4
        self._cost_weight = 0.4
        self.utility = 0
        self.rolling_sum_reward = 0
        self.rolling_sum_reward_320 = 0
        self.reward_value_accumilated = 0
        self._mean_power_allocation_3services_this_period = 0
        self._prev_mean_power_allocation_3services_this_period = 0
        self.occupancy_weight=0.5
        self.inverse_of_complement_wasting_requests_weight = 0.5
        self.perv_occupancy = 0
        self.derivation_occupancy_weight = 0.2
        self.derivation_wasting_requests_weight = 0.25
        self.remaining_requests_weight = 0.1
        self.perv_wasting_requests_ratio = 0
        self.prev_remaining_requests = 0
        self.remaining_services_threshold = 100


    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

    @property
    def prev_utility(self):
        return self._prev_utility

    @prev_utility.setter
    def prev_utility(self,value):
        self._prev_utility = value

    @property
    def mean_power_allocation_3services_this_period(self):
        return self._mean_power_allocation_3services_this_period

    @mean_power_allocation_3services_this_period.setter
    def mean_power_allocation_3services_this_period(self, value):
        self._mean_power_allocation_3services_this_period = value

    @property
    def prev_mean_power_allocation_3services_this_period(self):
        return self._prev_mean_power_allocation_3services_this_period

    @prev_mean_power_allocation_3services_this_period.setter
    def prev_mean_power_allocation_3services_this_period(self, value):
        self._prev_mean_power_allocation_3services_this_period = value
    @property
    def coeff(self):
        return self._coeff

    @coeff.setter
    def coeff(self, coeff_value):
        self._coeff = coeff_value

    @property
    def dx_t(self):
        return self._dx_t

    @dx_t.setter
    def dx_t(self, d):
        self._dx_t = d

    @property
    def dx_t_prev(self):
        return self._dx_t_prev

    @dx_t_prev.setter
    def dx_t_prev(self, d):
        self._dx_t_prev = d

    @property
    def services_requested(self):
        return self._services_requested

    @services_requested.setter
    def services_requested(self, value):
        self._services_requested = value

    @property
    def services_ensured(self):
        return self._services_ensured

    @services_ensured.setter
    def services_ensured(self, value):
        self._services_ensured = value


    @property
    def reward_value(self):
        return self._reward_value

    @reward_value.setter
    def reward_value(self, r):
        self._reward_value = r

    def calculate_utility(self):
        if (self.services_ensured ) == 0 and (
                self.services_requested ) == 0:
            return 0
        elif (self.services_ensured ) != 0 and (
                self.services_requested ) != 0:

            return self.services_ensured / self.services_requested
        else:
             return 0


    def resetreward(self):
        self.reward_value = 0
        # self.services_requested = 0
        # self.services_ensured = 0
        # self.utility = 0
        # self.prev_utility = 0
        # self._prev_mean_power_allocation_3services_this_period = 0
        # self._mean_power_allocation_3services_this_period = 0
        # self.reward_value_accumilated = 0

    def calculate_reward2(self,accepted,current_capacity,power_allocation):
        reward = -1
        if accepted == 1 and current_capacity >= power_allocation:
            return reward + 100
        elif accepted == 1 and  current_capacity < power_allocation:
            return reward -100
        elif accepted == 0 and current_capacity >= power_allocation:
            return reward - 100
        elif accepted == 0 and current_capacity < power_allocation:
            return reward



    def calculate_reward3(self,requested,ensured):
        if requested != 0 and ensured != 0 :
            self.utility = ensured / requested
        else :
            self.utility = 0
        derivation_throughput = self.utility - self._prev_utility
        # inv_cost = 0
        # inv_prev_cost = 0
        # if self._mean_power_allocation_3services_this_period ==  0 :
        #     inv_cost = 0
        # else :
        #     inv_cost = (1 / self._mean_power_allocation_3services_this_period)
        #
        # if self._prev_mean_power_allocation_3services_this_period == 0 :
        #     inv_prev_cost = 0
        # else:
        #     inv_prev_cost = (1 / self._prev_mean_power_allocation_3services_this_period)
        #
        # derivation_cost = inv_cost - inv_prev_cost
        # print("cost : ",self._mean_power_allocation_3services_this_period)
        # print("cost prev: ", self._prev_mean_power_allocation_3services_this_period)
        # print("1/cost : ",inv_cost)
        # print("1/cost normalized : ",(1/(1 + np.exp(-inv_cost))))
        # print("derivation_cost  : ", derivation_cost)
        # print("derivation normalized  : ",math.tanh(derivation_cost))
        if self.utility == 0.0:
            return -1
        else:
            return self._throughput_derivation_weight * math.tanh(derivation_throughput) + self._throughput_weight * self.utility \
                # + self._cost_weight * (1/(1 + np.exp(-inv_cost))) + \
                # self._cost_derivation_weight * math.tanh(derivation_cost)
    def calculate_reward(self, x, action, c, max_capacity):
        if action == 0:
            action = -1
        reward = 0
        if x > 0:
            if action == 1:
                reward = action * math.pow(math.sqrt(x / max_capacity), -1 * action)
                return reward
            elif action == -1:
                reward = action * math.pow(math.sqrt(x / max_capacity), -1 * action)
                return reward
        elif x < 0:
            alpha = 1 / c
            reward = -1 * action * math.pow(alpha, 2) * math.pow(x, 2)
            return reward
        elif x == 0:
            return 1

    def coefficient(self, max_capacity, power_allocated_service, action, request_supported):
        if max_capacity > power_allocated_service and action == 1 and request_supported == 1:
            return 2
        elif max_capacity < power_allocated_service and action == 0 and request_supported == 0:
            return 2
        elif max_capacity < power_allocated_service and action == 0 and request_supported == 1:
            return 1
        elif max_capacity > power_allocated_service and action == 0 and request_supported == 0:
            return 1
        elif max_capacity > power_allocated_service and action == 1 and request_supported == 0:
            return -1
        elif max_capacity > power_allocated_service and action == 0 and request_supported == 1:
            return -3
        elif max_capacity < power_allocated_service and action == 1 and request_supported == 1:
            return -1
        elif max_capacity < power_allocated_service and action == 1 and request_supported == 0:
            return -3
