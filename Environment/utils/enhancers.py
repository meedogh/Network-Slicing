from collections import deque

import numpy as np
import traci
import random as ra

from Utils.Bandwidth import Bandwidth
from Utils.Cost import RequestCost, TowerCost
from .aggregators import *
from .. import env_variables
from .mask_generation import *


def rolling_average(data, window_size):
    # Convert the data to a NumPy array with float type
    data_array = np.array(data, dtype=np.float64)
    # Calculate the rolling average using convolution with a window of ones
    weights = np.ones(window_size) / window_size
    rolling_avg = np.convolve(data_array, weights, mode='valid')
    # for i in range(len(data) - window_size + 1):
    #     window_sum = sum(data[i:i + window_size])
    #     rolling_avg = window_sum / window_size
    return rolling_avg


def centralize_state_action(gridcells_dqn, step, performance_logger):
    number_of_services = 3
    performance_logger.number_of_periods_until_now = 1

    for gridcell in gridcells_dqn:
        states = []
        actions = []
        actions_objects = []
        list_flags = []

        # if step > 2:
        #     if step > env_variables.advisor_period[0] and step <= env_variables.advisor_period[1]:
        #         flags = gridcell.agents.heuristic_action(gridcell,
        #                                                  performance_logger.outlet_services_power_allocation_for_all_requested,
        #                                                  performance_logger.outlet_services_requested_number,
        #                                                  performance_logger.number_of_periods_until_now)
        #         list_flags.extend(flags)
        for j, outlet in enumerate(gridcell.agents.grid_outlets):
            supported = []

            for i in range(number_of_services):
                gridcell.environment.state.index_outlet = j
                gridcell.environment.state.index_service = i
                if step <= 2:
                    list_flags.append(0)
                    gridcell.environment.state.max_capacity_each_outlet[
                        j
                    ] = outlet._max_capacity
                    gridcell.environment.state.capacity_each_tower[
                        j
                    ] = outlet.current_capacity
                    # gridcell.environment.state.services_requested_for_outlet = (
                    #     outlet.dqn.environment.state.services_requested
                    # )
                    # gridcell.environment.state.services_ensured_for_outlet = (
                    #     outlet.dqn.environment.state.services_ensured
                    # )
                    if len(outlet.power_distinct[0]) == 0:
                        outlet.power = [0.0, 0.0, 0.0]
                    gridcell.environment.state.allocated_power = outlet.power_distinct

                    state = gridcell.environment.state.calculate_state()
                    states.append(state)
                    action = ra.randint(0, 1)
                    actions.append(action)
                    gridcell.environment.state.supported_service = action
                    supported.append(action)

            count_zero = 0
            if step <= 2:
                for ind in range(3):
                    if supported[ind] == 0:
                        count_zero += 1
                if count_zero == 3:
                    supported[0] = 1
                outlet.supported_services = supported

            if step > 2:
                if (
                        step > env_variables.exploitation_exploration_period[0]
                        and step <= env_variables.exploitation_exploration_period[1]
                ):
                    outlet.supported_services = []
                    for serv_index in range(number_of_services):
                        action_centralize, action, flag = gridcell.agents.chain(
                            gridcell.model,
                            gridcell.environment.state.state_value_centralize[j],
                            [0, 1],
                            gridcell.agents.epsilon,
                        )

                        if isinstance(action, np.ndarray):
                            action = action.item()
                        outlet.supported_services.append(action)
                        list_flags.append(flag)

                if (
                        env_variables.advisor_period[0]
                        < step
                        <= env_variables.advisor_period[1]
                ):
                    # print("centralize exploit : .................................... ")
                    # if step > env_variables.advisor_period[0]  and  step <= env_variables.advisor_period[1]:
                    outlet.supported_services = []
                    for serv_index in range(number_of_services):
                        (
                            action_centralize,
                            action,
                            flag,
                        ) = gridcell.agents.exploitation(

                            gridcell.model,
                            gridcell.environment.state.state_value_centralize[j],
                        )
                        # actions_objects.append(action_centralize)
                        if isinstance(action, np.ndarray):
                            action = action.item()
                        outlet.supported_services.append(action)
                        list_flags.append(flag)

                actions.extend(outlet.supported_services)
            # print("outlet.supported_services : ", outlet.supported_services)
            outlet.dqn.environment.state.supported_services = outlet.supported_services

        # gridcell.agents.action.command.action_objects = actions_objects
        gridcell.agents.action.command.action_value_centralize = actions
        gridcell.agents.action.command.action_flags = list_flags

        if step <= 2:
            gridcell.environment.state.state_value_centralize = states


def centralize_nextstate_reward(gridcells_dqn):
    for gridcell in gridcells_dqn:
        next_states = []
        rewards = []
        utility_value_centralize = 0
        index_of_service = 0
        outlets = gridcell.agents.grid_outlets
        index_of_outlet = -1
        for i in range(9):
            index_of_service = i % 3
            if i % 3 == 0:
                index_of_outlet += 1

            gridcell.environment.state.index_service = index_of_service
            gridcell.environment.state.index_outlet = index_of_outlet
            gridcell.environment.state.max_capacity_each_outlet[
                index_of_service
            ] = outlets[index_of_outlet]._max_capacity
            gridcell.environment.state.capacity_each_tower[index_of_service] = outlets[
                index_of_outlet
            ].current_capacity
            # gridcell.environment.state.services_requested_for_outlet = outlets[
            #     index_of_outlet
            # ].dqn.environment.state.services_requested
            # gridcell.environment.state.services_ensured_for_outlet = outlets[
            #     index_of_outlet
            # ].dqn.environment.state.services_ensured
            gridcell.environment.state.allocated_power = outlets[
                index_of_outlet
            ].power_distinct
            next = gridcell.environment.state.calculate_state()
            next_states.append(next)
            # print("next state value centralize : ", next)

        rewards = gridcell.environment.reward.calculate_reward()

        gridcell.environment.state.next_state_centralize = next_states
        gridcell.environment.reward.reward_value = rewards
        # for index in range(9):
        #     gridcell.agents.remember(gridcell.agents.action.command.action_flags[index],
        #                              gridcell.environment.state.state_value_centralize[index],
        #                              gridcell.agents.action.command.action_value_centralize[index],
        #                              gridcell.environment.reward.reward_value[index],
        #                              gridcell.environment.state.next_state_centralize[index])

        gridcell.environment.state.state_value_centralize = (
            gridcell.environment.state.next_state_centralize
        )
        gridcell.environment.state.services_requested_prev = (
            gridcell.environment.state.services_requested
        )
        gridcell.environment.reward.services_requested_prev = (
            gridcell.environment.reward.services_requested
        )
        gridcell.environment.state.services_ensured_prev = (
            gridcell.environment.state.services_ensured
        )
        gridcell.environment.reward.services_ensured_prev = (
            gridcell.environment.reward.services_ensured
        )
        gridcell.environment.state.utility_value_centralize_prev = (
            utility_value_centralize
        )
        gridcell.environment.reward.utility_value_centralize_prev = (
            utility_value_centralize
        )



def serving_requests(performancelogger,outlet,start_time,service_):
        if outlet not in performancelogger.queue_provisioning_time_buffer:
            performancelogger.queue_provisioning_time_buffer[outlet] = dict()
        if outlet not in performancelogger.queue_requested_buffer:
            performancelogger.queue_requested_buffer[outlet] = deque([])
        if outlet not in performancelogger.queue_ensured_buffer:
            performancelogger.queue_ensured_buffer[outlet] = deque([])

        for i,(service, flag) in enumerate(performancelogger.queue_power_for_requested_in_buffer[outlet]):
            if service_==service :
                if flag == False :
                    if outlet.current_capacity >= service.service_power_allocate:
                        performancelogger.queue_power_for_requested_in_buffer[outlet][i][1] = True
                        performancelogger.queue_provisioning_time_buffer[outlet][service] = [start_time,
                                                                                             service.calcualate_processing_time()]
                        performancelogger.queue_ensured_buffer[outlet].appenleft(1)
                        outlet.current_capacity = outlet.current_capacity - service.service_power_allocate
                        return True
                    else :
                        return False
def provisioning_time_services(outlets, performance_logger, time_step_simulation):
    for i, outlet in enumerate(outlets):
        count = 0
        terminated_services = []
        for service, time in performance_logger.queue_provisioning_time_buffer[outlet].items():
            start_time = time[0]
            period_of_termination = time[1]
            if start_time + period_of_termination == time_step_simulation:
                count = count + 1
                terminated_services.append(service)
                outlet.current_capacity = outlet.current_capacity + service.service_power_allocate
        for service in terminated_services:
            performance_logger.queue_provisioning_time_buffer[outlet].pop(service)


def enable_sending_requests(car, observer, gridcells_dqn, performance_logger, start_time):
    car.attach(observer)
    car.set_state(
        float(round(traci.vehicle.getPosition(car.id)[0], 4)),
        float(round(traci.vehicle.getPosition(car.id)[1], 4)),
    )

    # car.add_satellite(outlets[-1])
    info = car.send_request()
    if info != None:
        outlet = info[0]
        service = info[1][2]
        if sum(outlet.supported_services) != 0:
            for gridcell in gridcells_dqn:
                for j, outlet_ in enumerate(gridcell.agents.grid_outlets):
                    if outlet == outlet_:
                        action = outlet_.dqn.agents.action.command.action_value_decentralize

                        service_index = service._dec_services_types_mapping[service.__class__.__name__]
                        print("action : ", action )

                        outlet.dqn.agents.action.command.action_object, outlet.dqn.agents.action.command.action_value_decentralize, flag = outlet.dqn.agents.chain_dec(
                            outlet.dqn.model,
                            outlet.dqn.environment.state.state_value_decentralize,
                            outlet.dqn.agents.epsilon,
                        )
                        if action == 1 and outlet.supported_services[service_index] == 1:
                            # print(action,"  ",service.request_supported(outlet)," ",outlet.current_capacity)
                            # performance_logger.queue_requested_buffer[outlet].appendleft(1)

                            request_bandwidth = Bandwidth(service.bandwidth, service.criticality)
                            request_cost = RequestCost(request_bandwidth, service.realtime)
                            request_cost.cost_setter(service.realtime)
                            service.service_power_allocate = request_bandwidth.allocated
                            performance_logger.queue_requested_buffer[outlet].appendleft(1)
                            performance_logger.queue_power_for_requested_in_buffer[outlet].appendleft(
                                [service, False])

                            performance_logger.queue_power_for_requested_in_buffer[outlet][0][1] = False
                            outlet._max_capacity = outlet.set_max_capacity(outlet.__class__.__name__)
                            gridcell.environment.state._max_capacity_each_outlet[j] = outlet._max_capacity
                            gridcell.environment.state._capacity_each_tower[j] = outlet.current_capacity


                            # outlet.dqn.environment.state.state_value_decentralize[0] =

                            outlet.dqn.environment.state.max_tower_capacity = outlet._max_capacity
                            outlet.dqn.environment.state._tower_capacity = outlet.current_capacity
                            outlet.dqn.environment.state.power_of_requests = service.service_power_allocate
                            if start_time == 0 :
                                outlet.dqn.environment.state.state_value_decentralize = outlet.dqn.environment.state.calculate_state()
                            print("state value : ", outlet.dqn.environment.state.state_value_decentralize)

                            print("action value : ",outlet.dqn.agents.action.command.action_value_decentralize)

                            served = serving_requests(performance_logger, outlet, start_time,service)

                            outlet.dqn.environment.state._tower_capacity = outlet.current_capacity
                            outlet.dqn.environment.state.power_of_requests = service.service_power_allocate

                            outlet.dqn.environment.state.next_state_decentralize = outlet.dqn.agents.action.command.action_object.execute(
                                outlet.dqn.environment.state,
                                outlet.dqn.agents.action.command.action_value_decentralize,
                            )

                            print("next state : ", outlet.dqn.environment.state.next_state_decentralize)
                            outlet.dqn.environment.reward.services_requested = len(performance_logger.queue_requested_buffer[outlet])
                            outlet.dqn.environment.reward.services_ensured = len(performance_logger.queue_ensured_buffer[outlet])

                            outlet.dqn.environment.reward.reward_value = outlet.dqn.environment.reward.calculate_reward2(
                                served,
                                outlet.current_capacity,
                                service.service_power_allocate

                            )

                            if outlet.dqn.environment.reward.service_requested == 0 and (
                                    outlet.dqn.agents.action.command.action_value_decentralize != 0):
                                remember_flag = False
                            else:
                                remember_flag = True

                            outlet.dqn.agents.remember_decentralize(
                                flag,
                                outlet.dqn.environment.state.state_value_decentralize,
                                outlet.dqn.agents.action.command.action_value_decentralize,
                                outlet.dqn.environment.reward.reward_value,
                                outlet.dqn.environment.state.next_state_decentralize,
                                remember_flag
                            )

                            outlet.dqn.environment.state.state_value_decentralize = outlet.dqn.environment.state.next_state_decentralize.copy()

