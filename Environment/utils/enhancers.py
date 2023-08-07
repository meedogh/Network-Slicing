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


def decentralize_reset(outlets, performance_logger,time_step_simulation):
    for i, outlet in enumerate(outlets):
        performance_logger.set_outlet_services_power_allocation_10_TimeStep(outlet,[0,0,0])
        # print(outlet.__class__.__name__)
        # print("befor resetting : ")
        # print("action : ", outlet.dqn.agents.action.command.action_value_decentralize)
        # print("current capacity : ", outlet.current_capacity)
        # print("requested buffer  : ", len(performance_logger.queue_requested_buffer[outlet]))
        # print("ensured buffer  : ", len(performance_logger.queue_ensured_buffer[outlet]))
        # print("len : ", len(performance_logger.queue_power_for_requested_in_buffer[outlet]))
        # count  = 0
        # print("befor ")
        # print("ensure    ", len(performance_logger.queue_ensured_buffer[outlet]))
        # print("req : ",len(performance_logger.queue_requested_buffer[outlet]))
        # print("serv : ",len(performance_logger.queue_power_for_requested_in_buffer[outlet]))

        for j in range(len(performance_logger.queue_ensured_buffer[outlet])):
            performance_logger.queue_requested_buffer[outlet].popleft()
            service, flag = performance_logger.queue_power_for_requested_in_buffer[outlet].popleft()
            # performance_logger.queue_provisioning_time_buffer.pop(service)
            del service
        performance_logger.queue_ensured_buffer[outlet].clear()
        # print("count >>>>>>>>>>>>>>>>>>>>>>>> ",count)
        # print("after resetting :....................................... ")
        # print("requested buffer  after : ", len(performance_logger.queue_requested_buffer[outlet]))
        # print("ensured buffer  after : ", len(performance_logger.queue_ensured_buffer[outlet]))
        # print("serv : ", len(performance_logger.queue_power_for_requested_in_buffer[outlet]))


def provisioning_time_services(outlets, performance_logger, time_step_simulation):
    for i, outlet in enumerate(outlets):
        # print("current befor terminate ", outlet.current_capacity)
        # print("befor outlet.dqn.environment.state.ratio_of_occupancy   : ",outlet.dqn.environment.state.ratio_of_occupancy)
        count = 0
        terminated_services = []
        # if performance_logger.queue_provisioning_time_buffer[outlet]:
        # print("len key : ", len(performance_logger.queue_provisioning_time_buffer[outlet].keys()))
        for service, time in performance_logger.queue_provisioning_time_buffer[outlet].items():
            start_time = time[0]
            period_of_termination = time[1]
            if start_time + period_of_termination == time_step_simulation:
                count = count + 1
                # print("service.service_power_allocate : ", service.service_power_allocate)
                # print("outlet.current_capacity : " ,outlet.current_capacity)
                terminated_services.append(service)
                outlet.current_capacity = outlet.current_capacity + service.service_power_allocate
        # print("count of serv     ",outlet.__class__.__name__, count)
        for service in terminated_services:
            performance_logger.queue_provisioning_time_buffer[outlet].pop(service)

            # print("current after terminate ", outlet.current_capacity, "   number of terminated services : " ,count )
            # print("after outlet.dqn.environment.state.ratio_of_occupancy   : ",outlet.dqn.environment.state.ratio_of_occupancy)



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
                        if sum(action) != 0:

                            service_index = service._dec_services_types_mapping[service.__class__.__name__]
                            # print("action ",action)
                            # if len(performance_logger.queue_requested_buffer[outlet]) > len(performance_logger.queue_ensured_buffer[outlet]) and len(performance_logger.queue_ensured_buffer[outlet])==0:
                            #     action = (0,0,0)
                            #     outlet.dqn.agents.action.command.action_value_decentralize = (0,0,0)
                            # # print("len(performance_logger.queue_requested_buffer[outlet]) : 1    ",len(performance_logger.queue_requested_buffer[outlet]))

                            if action[service_index] == 1 and outlet.supported_services[service_index] == 1:
                                # print(action,"  ",service.request_supported(outlet)," ",outlet.current_capacity)
                                performance_logger.queue_requested_buffer[outlet].appendleft(1)

                                # performance_logger.set_queue_provisioning_time_buffer(outlet,service, [0, 0])

                                request_bandwidth = Bandwidth(service.bandwidth, service.criticality)
                                request_cost = RequestCost(request_bandwidth, service.realtime)
                                request_cost.cost_setter(service.realtime)
                                service.service_power_allocate = request_bandwidth.allocated
                                # print("service.service_power_allocate : ",service.service_power_allocate)
                                power_aggregation(
                                    performance_logger.outlet_services_power_allocation,
                                    outlet,
                                    service.__class__.__name__,
                                    service,
                                    1,
                                )

                                services_aggregation(
                                    performance_logger.outlet_services_requested_number,
                                    outlet,
                                    service.__class__.__name__,
                                    1,
                                )

                                performance_logger.queue_power_for_requested_in_buffer[outlet].appendleft(
                                    [service, False])
                                # print(".... before ....  ",performance_logger.queue_power_for_requested_in_buffer[outlet])

                                performance_logger.queue_power_for_requested_in_buffer[outlet][0][1] = False
                                # print("req")
                                # print("action : ",outlet.dqn.agents.action.command.action_value_decentralize)
                                # print("action[service_index] : ", action[service_index])
                                # print("outlet.current_capacity : ",outlet.current_capacity)
                                # print("service.service_power_allocate : ",service.service_power_allocate)



def serving_requests(performancelogger,outlet,start_time):

        if outlet not in performancelogger.queue_provisioning_time_buffer:
            performancelogger.queue_provisioning_time_buffer[outlet] = dict()
        if outlet not in performancelogger.queue_requested_buffer:
            performancelogger.queue_requested_buffer[outlet]= deque([])

        print("len performance_logger.queue_requested_buffer[outlet] : ",
              len(performancelogger.queue_requested_buffer[outlet]))
        print("outlet ", outlet.__class__.__name__)
        print("outlet capacity : ", outlet.current_capacity)

        for i in range(len(performancelogger.queue_requested_buffer[outlet])):
            # print("len(performance_logger.queue_requested_buffer[outlet]): ",
            #       len(performancelogger.queue_requested_buffer[outlet]))
            # print("performance_logger.queue_power_for_requested_in_buffer[outlet].popleft(): ",
            #       len(performancelogger.queue_power_for_requested_in_buffer[outlet]))
            service, flag = performancelogger.queue_power_for_requested_in_buffer[outlet][i]
            # print("outlet.current_capacity : ", outlet.current_capacity)
            if outlet.current_capacity >= service.service_power_allocate:
                # performance_logger.queue_requested_buffer[outlet].popleft(1)
                performancelogger.queue_power_for_requested_in_buffer[outlet][i][1] = True
                performancelogger.queue_provisioning_time_buffer[outlet][service] = [start_time,
                                                                                     service.calcualate_processing_time()]
                ensured_service_aggrigation(
                    performancelogger.outlet_services_ensured_number,
                    outlet,
                    service.__class__.__name__,
                    1,

                )

                performancelogger.queue_ensured_buffer[outlet].appendleft(1)
                # extendleft([1] * len(performancelogger.queue_requested_buffer[outlet]))

                outlet.current_capacity = outlet.current_capacity - service.service_power_allocate
            print("len performance_logger.queue_ensured_buffer[outlet] : ",
                  len(performancelogger.queue_ensured_buffer[outlet]))
            print("outlet ", outlet.__class__.__name__)
            print("after ensuring outlet capacity : ", outlet.current_capacity)


def decentralize_state_action(performancelogger, gridcells_dqn, number_of_decentralize_periods, start_time):
    for gridcell in gridcells_dqn:
        for i, outlet in enumerate(gridcell.agents.grid_outlets):
            if sum(outlet.supported_services) != 0:

                # if outlet in performance_logger.handled_services:
                outlet._max_capacity = outlet.set_max_capacity(outlet.__class__.__name__)

                # outlet.dqn.environment.state.supported_services = outlet.supported_services
                # outlet.dqn.environment.state.action_value = outlet.dqn.agents.action_value

                if number_of_decentralize_periods == 0:
                    gridcell.environment.state._max_capacity_each_outlet[i] = outlet._max_capacity
                    gridcell.environment.state._capacity_each_tower[i] = outlet.current_capacity

                    ratio_of_occupancy = 0

                    outlet.dqn.environment.state.state_value_decentralize[0] = ratio_of_occupancy

                    outlet.dqn.environment.state.ratio_of_occupancy = ratio_of_occupancy
                    outlet.dqn.environment.state.max_tower_capacity = outlet._max_capacity
                    # print("first time ", ratio_of_occupancy)
                    for i in range(3):
                        outlet.dqn.environment.state._mean_power_allocated_requests[i] = \
                            performancelogger.outlet_services_power_allocation[outlet][
                                i] / number_of_decentralize_periods

                    outlet.dqn.environment.state.services_requested = len(
                        performancelogger.queue_requested_buffer[outlet]) - len(
                        performancelogger.queue_ensured_buffer[outlet])

                    outlet.dqn.environment.state.number_requested_in_period = len(
                        performancelogger.queue_requested_buffer[outlet])
                    outlet.dqn.environment.state.number_ensured_in_period = len(
                        performancelogger.queue_ensured_buffer[outlet])

                    outlet.dqn.environment.state.state_value_decentralize = outlet.dqn.environment.state.calculate_state()
                    #
                    # print(" outlet.dqn.environment.state.state_value_decentralize  : ",
                    #       outlet.dqn.environment.state.state_value_decentralize)
                # print(
                #     "decenlraize  state value :   ",
                #     outlet.dqn.environment.state.state_value_decentralize,
                # )
                outlet.dqn.agents.mask = action_masking(outlet.dqn.environment.state.supported_services)

                outlet.dqn.agents.action.command.action_object, outlet.dqn.agents.action.command.action_value_decentralize, flag = outlet.dqn.agents.chain_dec(
                    outlet.dqn.model,
                    outlet.dqn.environment.state.state_value_decentralize,
                    outlet.dqn.agents.mask,
                    outlet.dqn.agents.epsilon,
                )

                mapped_action = 0
                for key, val in action_permutations_dectionary.items():
                    if val == outlet.dqn.agents.action.command.action_value_decentralize:
                        # print("the key : ", key)
                        mapped_action = key
                outlet.dqn.agents.action.command.action_value_decentralize = mapped_action

                # if number_of_decentralize_periods >= 25:
                #     print("> = 25 ")
                #     outlet.dqn.agents.action.command.action_value_decentralize = (0,0,0)
                # print("outlet.dqn.agents.action.command.action_value_decentralize : ", outlet.dqn.agents.action.command.action_value_decentralize)

                # print("action : ", outlet.dqn.agents.action.command.action_value_decentralize)
                # print("supported : ", outlet.dqn.environment.state.supported_services)
                # print("outlet.dqn.agents.mask : ", outlet.dqn.agents.mask)

                outlet.dqn.agents.action_value = (
                    outlet.dqn.agents.action.command.action_value_decentralize
                )
            if sum(outlet.dqn.agents.action.command.action_value_decentralize) == 0:
                if len(performancelogger.queue_ensured_buffer[outlet]) == 0:
                    # print("cap ", outlet.current_capacity)

                    serving_requests(performancelogger,outlet,start_time)


def decentralize_nextstate_reward(gridcells_dqn, performancelogger, number_of_decentralize_periods):
    for gridcell in gridcells_dqn:
        for i, outlet in enumerate(gridcell.agents.grid_outlets):
            if sum(outlet.supported_services) != 0:

                # print("outlet._max_capacity : ",outlet._max_capacity)
                ratio_of_occupancy = (outlet._max_capacity - outlet.current_capacity) / outlet._max_capacity
                outlet.dqn.environment.state.ratio_of_occupancy = ratio_of_occupancy
                # print("ratio_of_occupancy : ",ratio_of_occupancy)

                outlet.dqn.environment.state.services_requested = len(
                    performancelogger.queue_requested_buffer[outlet]) - len(
                    performancelogger.queue_ensured_buffer[outlet])
                # print("len(performancelogger.queue_requested_buffer[outlet]) : ", len(performancelogger.queue_requested_buffer[outlet]))
                for i in range(3):
                    outlet.dqn.environment.state._mean_power_allocated_requests[i] = \
                        performancelogger.outlet_services_power_allocation[outlet][i] / number_of_decentralize_periods

                    outlet.dqn.environment.state.number_requested_in_period = len(
                        performancelogger.queue_requested_buffer[outlet])
                    outlet.dqn.environment.state.number_ensured_in_period = len(
                        performancelogger.queue_ensured_buffer[outlet])

                # print("power : ", performancelogger.outlet_services_power_allocation)
                # print("number_of_decentralize_periods : ", number_of_decentralize_periods)

                outlet.dqn.environment.state.next_state_decentralize = outlet.dqn.agents.action.command.action_object.execute(
                    outlet.dqn.environment.state,
                    outlet.dqn.agents.action.command.action_value_decentralize,
                )
                # print(
                #     "decenlraize next state value :",
                #     outlet.dqn.environment.state.next_state_decentralize,
                # )
                # print("len(performancelogger.queue_requested_buffer[outlet]) : ",len(performancelogger.queue_requested_buffer[outlet]))
                outlet.dqn.environment.reward.service_requested = len(performancelogger.queue_requested_buffer[outlet])
                # print("outlet.dqn.environment.reward.service_requested ",outlet.dqn.environment.reward.service_requested)
                outlet.dqn.environment.reward.service_ensured = len(performancelogger.queue_ensured_buffer[outlet])
                # if sum(performancelogger._outlet_services_power_allocation_10_TimeStep[outlet]) != 0 :
                #     outlet.dqn.environment.reward._mean_power_allocation_3services_this_period = \
                #         sum(performancelogger._outlet_services_power_allocation_10_TimeStep[outlet])/outlet.dqn.environment.reward.service_ensured
                # else :
                #     outlet.dqn.environment.reward._mean_power_allocation_3services_this_period = 0
                invers_of_complement_waisted_requests = 0
                if outlet.dqn.environment.reward.service_requested != 0:
                    invers_of_complement_waisted_requests = (
                    outlet.dqn.environment.reward.service_ensured / outlet.dqn.environment.reward.service_requested) - 1
                else:
                    invers_of_complement_waisted_requests = 0
                #
                # print("served num : ",outlet.dqn.environment.reward.service_ensured)
                # print("accepted : ",outlet.dqn.environment.reward.service_requested)
                outlet.dqn.environment.reward.reward_value = outlet.dqn.environment.reward.calculate_reward2(
                    ratio_of_occupancy,
                    invers_of_complement_waisted_requests

                )
                if outlet.dqn.environment.reward.service_requested != 0 and outlet.dqn.environment.reward.service_ensured != 0:
                    outlet.dqn.environment.reward.utility = outlet.dqn.environment.reward.service_ensured / outlet.dqn.environment.reward.service_requested
                else:
                    outlet.dqn.environment.reward.utility = 0
                outlet.dqn.environment.reward.reward_value_accumilated = outlet.dqn.environment.reward.reward_value_accumilated + outlet.dqn.environment.reward.reward_value
                # print("reward : ",outlet.dqn.environment.reward.reward_value )

                outlet.dqn.environment.reward._episode_reward_decentralize.append(
                    outlet.dqn.environment.reward.reward_value)

                flag = 1
                # print(" remember after mapping  : ", outlet.dqn.agents.action.command.action_value_decentralize)
                if outlet.dqn.environment.reward.service_requested == 0 and (
                        sum(outlet.dqn.agents.action.command.action_value_decentralize) != 0):
                    remember_flag = False
                else:
                    remember_flag = True
                # print("supported : ",outlet.supported_services)
                outlet.dqn.agents.remember_decentralize(
                    outlet.dqn.agents.mask,
                    flag,
                    outlet.dqn.environment.state.state_value_decentralize,
                    outlet.dqn.agents.action.command.action_value_decentralize,
                    outlet.dqn.environment.reward.reward_value,
                    outlet.dqn.environment.state.next_state_decentralize,
                    remember_flag
                )
                outlet.dqn.environment.state.state_value_decentralize = outlet.dqn.environment.state.next_state_decentralize.copy()

                if number_of_decentralize_periods % 32 == 0:
                    outlet.dqn.environment.state.state_value_decentralize = [0] * 7

                # print("state : ",outlet.dqn.environment.state.state_value_decentralize)
                # print("outlet.dqn.environment.state.state_value_decentralize after assingment : ",outlet.dqn.environment.state.state_value_decentralize)
                outlet.dqn.environment.reward.prev_utility = outlet.dqn.environment.reward.utility
                # outlet.dqn.environment.reward.prev_mean_power_allocation_3services_this_period = outlet.dqn.environment.reward._mean_power_allocation_3services_this_period
                # print("outlet.dqn.environment.reward._prev_mean_power_allocation_3services_this_period  : ", outlet.dqn.environment.reward._prev_mean_power_allocation_3services_this_period )
                outlet.dqn.environment.reward.perv_occupancy = ratio_of_occupancy
                outlet.dqn.environment.reward.perv_wasting_requests_ratio = invers_of_complement_waisted_requests


