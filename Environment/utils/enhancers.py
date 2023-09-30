import random
from collections import deque
import traci
import random as ra
from scipy.stats import beta
from Utils.Bandwidth import Bandwidth
from Utils.Cost import RequestCost, TowerCost
from .logging_rl import logging_important_info_for_testing
from .mask_generation import *


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
                outlet.supported_services = [1, 1, 1]

            if step > 2:
                # if (
                #         step > env_variables.exploitation_exploration_period[0]
                #         and step <= env_variables.exploitation_exploration_period[1]
                # ):
                outlet.supported_services = []
                for serv_index in range(number_of_services):
                    action_centralize, action, flag = gridcell.agents.chain(
                        gridcell.model,
                        gridcell.environment.state.state_value_centralize[j],
                        gridcell.agents.epsilon,
                    )

                    if isinstance(action, np.ndarray):
                        action = action.item()
                    outlet.supported_services.append(action)
                    list_flags.append(flag)

                # if (
                #         env_variables.advisor_period[0]
                #         < step
                #         <= env_variables.advisor_period[1]
                # ):
                #     # print("centralize exploit : .................................... ")
                #     # if step > env_variables.advisor_period[0]  and  step <= env_variables.advisor_period[1]:
                #     outlet.supported_services = []
                #     for serv_index in range(number_of_services):
                #         (
                #             action_centralize,
                #             action,
                #             flag,
                #         ) = gridcell.agents.exploitation(
                #
                #             gridcell.model,
                #             gridcell.environment.state.state_value_centralize[j],
                #         )
                #         # actions_objects.append(action_centralize)
                #         if isinstance(action, np.ndarray):
                #             action = action.item()
                #         outlet.supported_services.append(action)
                #         list_flags.append(flag)
                # centralize random actions for supported services
                if sum(outlet.supported_services) == 0:
                    while True:
                        a = random.randint(0, 1)
                        b = random.randint(0, 1)
                        c = random.randint(0, 1)
                        if a != 0 or b != 0 or c != 0:
                            break

                    outlet.supported_services = [a, b, c]

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


def serving_requests(performancelogger, outlet, start_time, service_):
    if outlet not in performancelogger.queue_requests_with_execution_time_buffer:
        performancelogger.queue_requests_with_execution_time_buffer[outlet] = dict()
    if outlet not in performancelogger.queue_requested_buffer:
        performancelogger.queue_requested_buffer[outlet] = deque([])
    if outlet not in performancelogger.queue_ensured_buffer:
        performancelogger.queue_ensured_buffer[outlet] = deque([])

    for i, (service, flag) in enumerate(performancelogger.queue_power_for_requested_in_buffer[outlet]):
        if service_ == service:
            if flag == False:
                if outlet.current_capacity >= service.service_power_allocate:
                    performancelogger.queue_power_for_requested_in_buffer[outlet][i][1] = True
                    performancelogger.queue_requests_with_execution_time_buffer[outlet][service] = [start_time,
                                                                                                    service.time_execution]
                    performancelogger.queue_ensured_buffer[outlet].appendleft(1)
                    outlet.current_capacity = outlet.current_capacity - service.service_power_allocate
                    return True
                else:
                    return False


def provisioning_time_services(outlets, performance_logger, time_step_simulation):
    for i, outlet in enumerate(outlets):
        if outlet.__class__.__name__ == 'Wifi':
            count = 0

            terminated_services = []
            for service, time in performance_logger.queue_requests_with_execution_time_buffer[outlet].items():
                start_time = time[0]
                period_of_termination = time[1]
                if start_time + period_of_termination == time_step_simulation:
                    count = count + 1
                    terminated_services.append(service)
                    outlet.current_capacity = outlet.current_capacity + service.service_power_allocate
            for service in terminated_services:
                performance_logger.queue_requests_with_execution_time_buffer[outlet].pop(service)


def check_timed_out(performance_logger, outlet, request_time_out_period, demanding_time_step, request_power_allocation,
                    current_capacity):
    counter_can_executed = 0
    counter_cannt_executed = 0
    for service, time in performance_logger.queue_requests_with_execution_time_buffer[outlet].items():
        start_time = time[0]
        period_of_termination = time[1]
        if start_time + period_of_termination <= demanding_time_step:
            current_capacity += service.service_power_allocate

    for service, time in performance_logger.queue_waiting_requests_in_buffer[outlet]:
        start_time = performance_logger.queue_requests_with_time_out_buffer[outlet][service][0]
        time_out = performance_logger.queue_requests_with_time_out_buffer[outlet][service][1]
        if start_time + time_out >= demanding_time_step and current_capacity >= service.service_power_allocate:
            counter_can_executed += 1
            current_capacity -= service.service_power_allocate
        else:
            counter_cannt_executed += 1
    for service, time in performance_logger.queue_requests_with_execution_time_buffer[outlet].items():
        start_time = time[0]
        period_of_termination = time[1]
        timed_out_step_of_new_request = demanding_time_step + request_time_out_period
        if demanding_time_step <= start_time + period_of_termination < timed_out_step_of_new_request:
            current_capacity += service.service_power_allocate

    if current_capacity >= request_power_allocation:
        #round(((self._tower_capacity / self.max_tower_capacity) * 100), 2)
        return 0, round(((current_capacity/3500)*100),2 ) , round(((request_power_allocation/3500)*100),2 )
    else:
        return 1, round(((current_capacity/3500)*100),2 ) , round(((request_power_allocation/3500)*100),2 )


def buffering_not_served_requests(outlets, performancelogger, time_step_simulation, satellite):
    for outlet_index, outlet in enumerate(outlets):
        if outlet.__class__.__name__ == 'Wifi':
            services_timed_out = []
            service_moved_to_served = []
            # services = list(performancelogger.queue_waiting_requests_in_buffer[outlet])
            # services.sort(key=lambda ser: (ser[0].service_power_allocate, ser[0].time_out))
            # performancelogger.queue_waiting_requests_in_buffer[outlet] = deque(services)

            for i, (service, flag) in enumerate(performancelogger.queue_waiting_requests_in_buffer[outlet]):
                if flag == True:
                    failure_rate = 0.75
                    service.request_failure = np.random.rand() >= failure_rate
                    if service.request_failure == False:
                        outlet.dqn.agents.action.command.action_value_decentralize = 1
                        outlet.dqn.environment.state.max_tower_capacity = outlet._max_capacity
                        outlet.dqn.environment.state._tower_capacity = outlet.current_capacity
                        outlet.dqn.environment.state.power_of_requests = service.service_power_allocate
                        outlet.dqn.environment.state.waiting_buffer_len = len(
                            performancelogger.queue_waiting_requests_in_buffer[outlet])

                        start_time = performancelogger.queue_requests_with_time_out_buffer[outlet][service][0]
                        time_out = performancelogger.queue_requests_with_time_out_buffer[outlet][service][1]
                        outlet.dqn.environment.state.remaining_time_out = time_out
                        service.remaining_time_out = outlet.dqn.environment.state.remaining_time_out

                        lr = -1
                        if start_time + time_out <= time_step_simulation and len(
                                performancelogger.queue_waiting_requests_in_buffer[outlet]) > 0:
                            # print("time_out ",time_out)
                            # print("start_time + time_out : ", start_time + time_out)
                            # print("time_step_simulation : ", time_step_simulation)
                            outlet.dqn.environment.state.time_out_flag = 1
                            outlet.dqn.environment.state.tower_capacity_before_time_out_step_service = service.tower_capacity_before_time_out_step

                            outlet.dqn.environment.state.state_value_decentralize = outlet.dqn.environment.state.calculate_state(
                                45)
                            # add_value_to_pickle('C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//time_out_state.pkl',
                            #                     outlet.dqn.environment.state.state_value_decentralize)
                            # print("state time out  : ", outlet.dqn.environment.state.state_value_decentralize)

                            services_timed_out.append(service)
                            performancelogger.queue_time_out_from_simulation[outlet].appendleft([service, True])
                            outlet.dqn.environment.state.time_out_requests_over_simulation = len(
                                performancelogger.queue_time_out_from_simulation[outlet])
                            outlet.dqn.environment.state.remaining_time_out = 0
                            service.remaining_time_out = outlet.dqn.environment.state.remaining_time_out

                            outlet.dqn.environment.state.waiting_buffer_len = len(
                                performancelogger.queue_waiting_requests_in_buffer[outlet]) - (
                                                                                  len(services_timed_out)
                                                                              )
                            outlet.dqn.environment.state.timed_out_length = len(services_timed_out)
                            outlet.dqn.environment.state.from_waiting_to_serv_length = 0
                            outlet.dqn.environment.state.wasting_buffer_length = len(
                                performancelogger.queue_wasted_req_buffer[outlet])
                            outlet.dqn.environment.state.from_waiting_to_serv_length = 0
                            outlet.dqn.environment.state.tower_capacity_before_time_out_step_service = service.tower_capacity_before_time_out_step

                            outlet.dqn.environment.state.time_out_flag = 1
                            outlet.dqn.environment.state.next_state_decentralize = outlet.dqn.environment.state.calculate_state(
                                45)
                            # print("next state time out  : ", outlet.dqn.environment.state.next_state_decentralize)

                            outlet.dqn.environment.reward.reward_value = -2
                            outlet.dqn.environment.reward.time_out_reward += -2

                            outlet.dqn.environment.reward.reward_value_accumilated = outlet.dqn.environment.reward.reward_value_accumilated + outlet.dqn.environment.reward.reward_value
                            # print("outlet.dqn.environment.reward.reward_value_accumilated  : ",
                            #       outlet.dqn.environment.reward.reward_value_accumilated)

                            outlet.dqn.environment.state.delay_time = 0
                            logging_important_info_for_testing(performancelogger, outlet_index, outlet, satellite)

                            flag = 1
                            outlet.dqn.agents.remember_decentralize(
                                flag,
                                outlet.dqn.environment.state.state_value_decentralize,
                                outlet.dqn.agents.action.command.action_value_decentralize,
                                outlet.dqn.environment.reward.reward_value,
                                outlet.dqn.environment.state.next_state_decentralize,
                                0.0

                            )

                        elif start_time + time_out > time_step_simulation and outlet.current_capacity >= service.service_power_allocate and len(
                                performancelogger.queue_waiting_requests_in_buffer[outlet]) > 0:
                            service_moved_to_served.append(service)
                            outlet.sum_of_costs_of_all_requests += service.total_cost_in_dolar
                            performancelogger.queue_from_wait_to_serve_over_simulation[outlet].appendleft(
                                [service, True])
                            outlet.dqn.environment.state.from_wait_to_serve_over_simulation = len(
                                performancelogger.queue_from_wait_to_serve_over_simulation[outlet])

                            if [service, False] in performancelogger.queue_power_for_requested_in_buffer[outlet]:
                                index = performancelogger.queue_power_for_requested_in_buffer[outlet].index(
                                    [service, False])
                                performancelogger.queue_power_for_requested_in_buffer[outlet][index][1] = True

                            performancelogger.queue_requests_with_execution_time_buffer[outlet][service] = [start_time,
                                                                                                            service.time_execution]

                            for car, outlet_inner_dect in performancelogger.user_requests.items():
                                for outlet_name, services in outlet_inner_dect.items():
                                    for i, (ser, flag, cost) in enumerate(services):
                                        if service == ser and outlet_name == outlet.__class__.__name__:
                                            performancelogger.user_requests[car][outlet_name][i][0] = True
                                            performancelogger.user_requests[car][outlet_name][i][
                                                2] = service.total_cost_in_dolar

                            performancelogger.queue_ensured_buffer[outlet].appendleft(1)
                            outlet.dqn.environment.reward.services_requested = len(
                                performancelogger.queue_requested_buffer[outlet])
                            outlet.dqn.environment.reward.services_ensured = len(
                                performancelogger.queue_ensured_buffer[outlet])

                            outlet.dqn.environment.state.time_out_flag = 0
                            outlet.dqn.environment.state.tower_capacity_before_time_out_step_service = service.tower_capacity_before_time_out_step

                            outlet.dqn.environment.state.state_value_decentralize = outlet.dqn.environment.state.calculate_state(
                                45)
                            # print("action ", outlet.dqn.agents.action.command.action_value_decentralize)
                            # print("state wait to serve  : ", outlet.dqn.environment.state.state_value_decentralize)
                            # add_value_to_pickle(
                            #     'C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//wait_to_serve_state.pkl',
                            #     outlet.dqn.environment.state.state_value_decentralize)
                            outlet.current_capacity = outlet.current_capacity - service.service_power_allocate
                            outlet.dqn.environment.state._tower_capacity = outlet.current_capacity
                            outlet.dqn.environment.state.waiting_buffer_len = len(
                                performancelogger.queue_waiting_requests_in_buffer[outlet]) - len(
                                service_moved_to_served)

                            outlet.dqn.environment.state.from_waiting_to_serv_length = len(service_moved_to_served)
                            outlet.dqn.environment.state.timed_out_length = 0

                            outlet.dqn.environment.state.wasting_buffer_length = len(
                                performancelogger.queue_wasted_req_buffer[outlet])

                            outlet.dqn.environment.state.timed_out_length = 0
                            outlet.dqn.environment.state.wasting_buffer_length = len(
                                performancelogger.queue_wasted_req_buffer[outlet])
                            outlet.dqn.environment.state.remaining_time_out = time_out - (
                                    time_step_simulation - start_time) - 1

                            service.remaining_time_out = outlet.dqn.environment.state.remaining_time_out
                            # print("here service.remaining_time_out  : ", service.remaining_time_out)

                            outlet.dqn.environment.state.delay_time = time_out - outlet.dqn.environment.state.remaining_time_out
                            outlet.dqn.environment.state.time_out_flag = 0

                            outlet.dqn.environment.state.tower_capacity_before_time_out_step_service = service.tower_capacity_before_time_out_step - round(
                                ((service.service_power_allocate / 3500) * 100), 2)

                            outlet.dqn.environment.state.next_state_decentralize = outlet.dqn.environment.state.calculate_state(
                                45)
                            # print("next state wait to serve  : ", outlet.dqn.environment.state.next_state_decentralize)
                            # print("from wait to serve next state : ",outlet.dqn.environment.state.next_state_decentralize)
                            outlet.dqn.environment.reward.reward_value = 2
                            outlet.dqn.environment.reward.wait_to_serve_reward += 2

                            outlet.dqn.environment.reward.reward_value_accumilated = outlet.dqn.environment.reward.reward_value_accumilated + outlet.dqn.environment.reward.reward_value
                            # print("outlet.dqn.environment.reward.reward_value_accumilated  : ",
                            #       outlet.dqn.environment.reward.reward_value_accumilated)

                            logging_important_info_for_testing(performancelogger, outlet_index, outlet, satellite)

                            flag = 1
                            outlet.dqn.agents.remember_decentralize(
                                flag,
                                outlet.dqn.environment.state.state_value_decentralize,
                                outlet.dqn.agents.action.command.action_value_decentralize,
                                outlet.dqn.environment.reward.reward_value,
                                outlet.dqn.environment.state.next_state_decentralize,
                                0.0
                            )

            for ser in services_timed_out:
                performancelogger.queue_waiting_requests_in_buffer[outlet].remove([ser, True])
            choosing_abort_requests(performancelogger, outlet)
            for ser in service_moved_to_served:
                if ser in performancelogger.queue_waiting_requests_in_buffer[outlet]:
                    performancelogger.queue_waiting_requests_in_buffer[outlet].remove([ser, True])


def choosing_abort_requests(performance_logger, outlet):
    alpha = 1
    beta_value = 3
    # Generate random probabilities from the beta distribution
    timeout_durations = []
    remaining_time_out_duration = []
    # Normalize the timeout durations between 0 and 1 for the beta distribution
    for i, (service, flag) in enumerate(performance_logger.queue_waiting_requests_in_buffer[outlet]):
        if flag == True:
            timeout_durations.append(service.time_out)
            remaining_time_out_duration.append(service.remaining_time_out)
    normalized_timeouts = [1 - (el2 / el1) for el1, el2 in zip(timeout_durations, remaining_time_out_duration)]
    # Calculate the percent point function (inverse of the CDF)
    vals = beta.ppf(normalized_timeouts, alpha, beta_value)
    aborted_services = []
    for i, (service, flag) in enumerate(performance_logger.queue_waiting_requests_in_buffer[outlet]):
        if flag == True:
            if vals[i] >= 0.3:
                aborted_services.append(service)
    outlet.abort_requests += len(aborted_services)
    for ser in aborted_services:
        performance_logger.queue_waiting_requests_in_buffer[outlet].remove([ser, True])


def outlet_max_waiting_buffer_length(outlet):
    if outlet.__class__.__name__ == 'Wifi':
        return 45
    if outlet.__class__.__name__ == 'ThreeG':
        return 125
    if outlet.__class__.__name__ == 'FourG':
        return 250
    if outlet.__class__.__name__ == 'FiveG':
        return 500


def request_reject_acceptance(car, performance_logger, gridcells_dqn, outlet, service, start_time, satellite, info):
    # print(" outlet.supported_services  :  ", outlet.supported_services)
    if sum(outlet.supported_services) != 0:
        for gridcell in gridcells_dqn:
            for j, outlet_ in enumerate(gridcell.agents.grid_outlets):
                if outlet == outlet_:
                    # print("equals outlets : ")
                    service_index = service._dec_services_types_mapping[service.__class__.__name__]
                    # outlet.__class__.__name__ == 'Wifi'  and
                    if outlet.__class__.__name__ == 'Wifi' and outlet.supported_services[service_index] == 1:
                        if len(performance_logger.queue_waiting_requests_in_buffer[
                                   outlet]) < outlet_max_waiting_buffer_length(outlet):
                            request_bandwidth = Bandwidth(service.bandwidth, service.criticality)
                            request_cost = RequestCost(request_bandwidth, service.realtime)
                            # request_cost.cost_setter(service.realtime)
                            service.cost_in_bit_rate = request_cost.cost_setter(outlet)
                            service.service_power_allocate = request_bandwidth.allocated
                            service.total_cost_in_dolar = service.calculate_service_cost_in_Dolar_per_bit()
                            outlet._max_capacity = outlet.set_max_capacity(outlet.__class__.__name__)
                            gridcell.environment.state._max_capacity_each_outlet[j] = outlet._max_capacity
                            gridcell.environment.state._capacity_each_tower[j] = outlet.current_capacity
                            outlet.dqn.environment.state.max_tower_capacity = outlet._max_capacity
                            outlet.dqn.environment.state._tower_capacity = outlet.current_capacity
                            outlet.dqn.environment.state.power_of_requests = service.service_power_allocate
                            outlet.dqn.environment.state.waiting_buffer_len = len(
                                performance_logger.queue_waiting_requests_in_buffer[outlet])

                            service.time_out = service.calculate_time_out()
                            service.time_execution = service.calculate_processing_time()

                            # path = f"{request_info}outlet_{outlet.__class__.__name__}.pkl"
                            # main_string = service.__class__.__name__
                            #
                            # substring_dec = {'Safety': "SAFETY",
                            #                  'Entertainment': "ENTERTAINMENT",
                            #                  'Autonomous': "AUTONOMOUS"}
                            #
                            # for key, value1 in substring_dec.items():
                            #     if key in main_string:
                            #         value = (value1, service.service_power_allocate, service.time_out,
                            #                  service.time_execution, start_time)
                            #         add_value_to_pickle(path, value)
                            service.remaining_time_out = outlet.dqn.environment.state.remaining_time_out
                            outlet.dqn.environment.state.remaining_time_out = service.time_out
                            service.remaining_time_out = outlet.dqn.environment.state.remaining_time_out

                            outlet.dqn.environment.state.time_out_flag = 0

                            # if len(performance_logger.queue_waiting_requests_in_buffer) > 0:
                            # outlet.dqn.environment.state.time_out_flag,copy_of_capacity,req_power = check_timed_out(performance_logger,
                            #                                                          outlet,
                            #                                                          service.time_out,
                            #                                                          start_time,
                            #                                                          service.service_power_allocate,
                            #                                                          outlet.current_capacity)
                            #
                            # print("flag  : " , outlet.dqn.environment.state.time_out_flag,"   ",copy_of_capacity,"   ",req_power ,"  ",outlet._max_capacity)
                            # # service.tower_capacity_before_time_out_step  =  copy_of_capacity
                            # service.tower_capacity_before_time_out_step = copy_of_capacity

                            # else:
                            #     outlet.dqn.environment.state.time_out_flag = 0

                            if outlet.dqn.environment.state.time_out_flag == 1:
                                outlet.dqn.environment.state.number_of_timed_out_requests_from_algorithm += 1

                            if outlet.dqn.environment.state.time_out_flag == 0:
                                outlet.dqn.environment.state.tower_capacity_before_time_out_step_service = service.tower_capacity_before_time_out_step
                                outlet.dqn.environment.state.state_value_decentralize = outlet.dqn.environment.state.calculate_state(
                                    45)
                                lr = -1

                                outlet.dqn.agents.action.command.action_object, outlet.dqn.agents.action.command.action_value_decentralize, flag = outlet.dqn.agents.chain_dec(
                                    outlet.dqn.model,
                                    outlet.dqn.environment.state.state_value_decentralize,
                                    outlet.dqn.agents.epsilon,
                                )
                                action = outlet.dqn.agents.action.command.action_value_decentralize
                                # print("action is .................... : ", action )
                                if action == 0:
                                    # print("rejecting state : ",
                                    #       outlet.dqn.environment.state.state_value_decentralize)
                                    outlet.dqn.environment.state._tower_capacity = outlet.current_capacity
                                    outlet.dqn.environment.state.power_of_requests = service.service_power_allocate
                                    outlet.dqn.environment.state.waiting_buffer_len = len(
                                        performance_logger.queue_waiting_requests_in_buffer[outlet])

                                    outlet.dqn.environment.state.remaining_time_out = service.time_out
                                    service.remaining_time_out = outlet.dqn.environment.state.remaining_time_out
                                    outlet.dqn.environment.state.tower_capacity_before_time_out_step_service = service.tower_capacity_before_time_out_step

                                    outlet.dqn.environment.state.next_state_decentralize = outlet.dqn.agents.action.command.action_object.execute(
                                        outlet.dqn.environment.state,
                                        outlet.dqn.agents.action.command.action_value_decentralize,
                                    )

                                    # print("rejecting next state : ", outlet.dqn.environment.state.next_state_decentralize)
                                    outlet.dqn.environment.reward.reward_value = lr
                                    outlet.dqn.environment.reward.rejected_reward += -1
                                    # print("outlet.dqn.environment.reward.reward_value_accumilated  : ", outlet.dqn.environment.reward.reward_value_accumilated)
                                    outlet.dqn.environment.reward.reward_value_accumilated = outlet.dqn.environment.reward.reward_value_accumilated + outlet.dqn.environment.reward.reward_value
                                    outlet.dqn.environment.state.timed_out_length = 0
                                    outlet.dqn.environment.state.waiting_buffer_len = len(
                                        performance_logger.queue_waiting_requests_in_buffer[outlet])
                                    outlet.dqn.environment.state.from_waiting_to_serv_length = 0
                                    outlet.dqn.environment.state.wasting_buffer_length = len(
                                        performance_logger.queue_wasted_req_buffer[outlet])
                                    outlet.dqn.environment.state.delay_time = 0

                                    logging_important_info_for_testing(performance_logger, j, outlet, satellite)

                                    outlet.dqn.agents.remember_decentralize(
                                        flag,
                                        outlet.dqn.environment.state.state_value_decentralize,
                                        outlet.dqn.agents.action.command.action_value_decentralize,
                                        outlet.dqn.environment.reward.reward_value,
                                        outlet.dqn.environment.state.next_state_decentralize,
                                        0.0

                                    )

                                    if len(info[0]) == 2:
                                        outlet2 = info[0][1]
                                        info[0].pop(0)
                                        performance_logger.set_user_requests(outlet2, car, service, False)
                                        request_reject_acceptance(car, performance_logger, gridcells_dqn, outlet2,
                                                                  service,
                                                                  start_time, satellite, info)

                                    else:
                                        service.cost_in_bit_rate = request_cost.cost_setter(satellite)
                                        service.service_power_allocate = request_bandwidth.allocated
                                        service.total_cost_in_dolar = service.calculate_service_cost_in_Dolar_per_bit()
                                        satellite.rejected_requests_buffer.append(service)
                                        satellite.sum_of_costs_of_all_requests += service.total_cost_in_dolar
                                        performance_logger.set_user_requests(satellite, car, service, False)
                                        for car, outlet_inner_dect in performance_logger.user_requests.items():
                                            for outlet_name, services in outlet_inner_dect.items():
                                                for i, (ser, flag, cost) in enumerate(services):
                                                    if service == ser and outlet_name == satellite.__class__.__name__:
                                                        performance_logger.user_requests[car][outlet_name][i][1] = True
                                                        performance_logger.user_requests[car][outlet_name][i][
                                                            2] = service.total_cost_in_dolar
                                        break

                                if action == 1 and len(
                                        performance_logger.queue_waiting_requests_in_buffer[outlet]) == 0:
                                    # print("action ", action)
                                    performance_logger.queue_requested_buffer[outlet].appendleft(1)

                                    performance_logger.queue_power_for_requested_in_buffer[outlet].append(
                                        [service, False])

                                    performance_logger.queue_power_for_requested_in_buffer[outlet][0][1] = False

                                    served = serving_requests(performance_logger, outlet, start_time, service)

                                    if served == True:
                                        # print("state serve : ", outlet.dqn.environment.state.state_value_decentralize)
                                        outlet.dqn.environment.state._tower_capacity = outlet.current_capacity
                                        outlet.dqn.environment.state.power_of_requests = service.service_power_allocate

                                        # print("served state : ",
                                        #       outlet.dqn.environment.state.state_value_decentralize)
                                        outlet.sum_of_costs_of_all_requests += service.total_cost_in_dolar

                                        for car, outlet_inner_dect in performance_logger.user_requests.items():
                                            for outlet_name, services in outlet_inner_dect.items():
                                                for i, (ser, flag, cost) in enumerate(services):
                                                    if service == ser and outlet_name == outlet.__class__.__name__:
                                                        performance_logger.user_requests[car][outlet_name][i][1] = True
                                                        performance_logger.user_requests[car][outlet_name][i][
                                                            2] = service.total_cost_in_dolar

                                        outlet.dqn.environment.state.waiting_buffer_len = len(
                                            performance_logger.queue_waiting_requests_in_buffer[outlet])

                                        outlet.dqn.environment.state.remaining_time_out = service.time_out
                                        service.remaining_time_out = outlet.dqn.environment.state.remaining_time_out

                                        outlet.dqn.environment.state.time_out_flag = 0

                                        # outlet.dqn.environment.state.tower_capacity_before_time_out_step_service = service.tower_capacity_before_time_out_step - round(((service.service_power_allocate/3500)*100),2)
                                        outlet.dqn.environment.state.next_state_decentralize = outlet.dqn.agents.action.command.action_object.execute(
                                            outlet.dqn.environment.state,
                                            outlet.dqn.agents.action.command.action_value_decentralize,
                                        )
                                        # print("serving next state : ",
                                        #       outlet.dqn.environment.state.next_state_decentralize)
                                        outlet.dqn.environment.reward.services_requested = len(
                                            performance_logger.queue_requested_buffer[outlet])
                                        outlet.dqn.environment.reward.services_ensured = len(
                                            performance_logger.queue_ensured_buffer[outlet])

                                        outlet.dqn.environment.reward.reward_value = 2
                                        outlet.dqn.environment.reward.serving_reward += 2

                                        outlet.dqn.environment.reward.reward_value_accumilated = outlet.dqn.environment.reward.reward_value_accumilated + outlet.dqn.environment.reward.reward_value
                                        # print("outlet.dqn.environment.reward.reward_value_accumilated  : ", outlet.dqn.environment.reward.reward_value_accumilated)

                                    outlet.dqn.environment.state.timed_out_length = 0
                                    outlet.dqn.environment.state.from_waiting_to_serv_length = 0
                                    outlet.dqn.environment.state.wasting_buffer_length = len(
                                        performance_logger.queue_wasted_req_buffer[outlet])
                                    outlet.dqn.environment.state.delay_time = 0

                                    logging_important_info_for_testing(performance_logger, j, outlet, satellite)

                                    outlet.dqn.agents.remember_decentralize(
                                        flag,
                                        outlet.dqn.environment.state.state_value_decentralize,
                                        outlet.dqn.agents.action.command.action_value_decentralize,
                                        outlet.dqn.environment.reward.reward_value,
                                        outlet.dqn.environment.state.next_state_decentralize,
                                        0.0

                                    )
                                    if served == False:
                                        performance_logger.queue_waiting_requests_in_buffer[outlet].appendleft(
                                            [service, True])
                                        performance_logger.queue_requests_with_time_out_buffer[outlet][service] = [
                                            start_time,
                                            service.time_out]

                                if action == 1 and len(
                                        performance_logger.queue_waiting_requests_in_buffer[outlet]) != 0 \
                                        and len(performance_logger.queue_waiting_requests_in_buffer[
                                                    outlet]) <= outlet_max_waiting_buffer_length(outlet):
                                    performance_logger.queue_requested_buffer[outlet].appendleft(1)

                                    outlet.dqn.environment.reward.services_requested = len(
                                        performance_logger.queue_requested_buffer[outlet])
                                    outlet.dqn.environment.reward.services_ensured = len(
                                        performance_logger.queue_ensured_buffer[outlet])

                                    performance_logger.queue_power_for_requested_in_buffer[outlet].append(
                                        [service, False])

                                    performance_logger.queue_power_for_requested_in_buffer[outlet][0][1] = False

                                    performance_logger.queue_waiting_requests_in_buffer[outlet].appendleft(
                                        [service, True])
                                    performance_logger.queue_requests_with_time_out_buffer[outlet][service] = [
                                        start_time,
                                        service.time_out]

                                if len(performance_logger.queue_waiting_requests_in_buffer[outlet]) != 0 \
                                        and len(performance_logger.queue_waiting_requests_in_buffer[
                                                    outlet]) >= outlet_max_waiting_buffer_length(outlet):
                                    performance_logger.queue_wasted_req_buffer[outlet].appendleft(
                                        [service, True])
                                    outlet.dqn.environment.state.wasting_buffer_length = len(
                                        performance_logger.queue_wasted_req_buffer[outlet])
                        if outlet.__class__.__name__ == 'Wifi' and len(
                                performance_logger.queue_waiting_requests_in_buffer[outlet]) != 0 \
                                and len(performance_logger.queue_waiting_requests_in_buffer[
                                            outlet]) >= outlet_max_waiting_buffer_length(outlet):
                            performance_logger.queue_wasted_req_buffer[outlet].appendleft(
                                [service, True])
                            outlet.dqn.environment.state.wasting_buffer_length = len(
                                performance_logger.queue_wasted_req_buffer[outlet])


def enable_sending_requests(car, observer, gridcells_dqn, performance_logger, start_time, satellite):
    car.attach(observer)
    car.set_state(
        float(round(traci.vehicle.getPosition(car.id)[0], 4)),
        float(round(traci.vehicle.getPosition(car.id)[1], 4)), )
    info = car.send_request()
    if info != None:
        outlet = info[0][0]
        service = info[1][2]
        performance_logger.set_user_requests(outlet, car, service, False)
        performance_logger.generated_requests_over_simulation.appendleft(1)
        request_reject_acceptance(car, performance_logger, gridcells_dqn, outlet, service, start_time, satellite, info)
