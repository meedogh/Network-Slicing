import os
import pickle
from .aggregators import *


def add_value_to_pickle(path, value):
    mode = "wb" if not os.path.exists(path) else "ab"
    with open(path, mode) as file:
        pickle.dump(value, file)

def accumulate_until_sum_limit(lst, target_sum):
    accumulated_values = []
    current_sum = 0
    counter = 0

    for value in reversed(lst):
        if current_sum + value <= target_sum:
            counter += 1
            accumulated_values.append(value)
            current_sum += value

            if current_sum == target_sum:
                break

    return accumulated_values[::-1], counter


def terminate_service(veh, outlets, performance_logger):
    for out in outlets:
        if out not in veh.outlets_serve:
            if out in performance_logger.handled_services:
                if veh in performance_logger.handled_services[out]:
                    print("terminate second condition ")
                    serv = performance_logger.handled_services[out][veh]
                    services_aggregation(
                        performance_logger.outlet_services_requested_number,
                        out,
                        serv.__class__.__name__,
                        -1,
                    )

                    ensured_service_aggrigation(
                        performance_logger.outlet_services_ensured_number,
                        out,
                        serv.__class__.__name__,
                        -1,
                    )
                    power_aggregation(
                        performance_logger.outlet_services_power_allocation,
                        out,
                        serv.__class__.__name__,
                        serv,
                        -1,
                    )
                    if (
                        out.current_capacity + serv.service_power_allocate
                        < out._max_capacity
                    ):
                        out.current_capacity = (
                            out.current_capacity + serv.service_power_allocate
                        )
                        if out.current_capacity >= out._max_capacity:
                            out.current_capacity = out._max_capacity
                        removed_value = performance_logger.handled_services[out].pop(
                            veh
                        )
                        del removed_value
                        del serv

        else:
            out.current_capacity = out.current_capacity
