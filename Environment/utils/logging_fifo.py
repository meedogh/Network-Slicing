import os

from Environment.utils.helpers import add_value_to_pickle
from Environment.utils.paths import *

def logging_important_info_for_testing_fifo(performance_logger_for_fifo,
        outlet_index,outlet ):


    add_value_to_pickle(
        os.path.join(requested_decentralized_path, f"requested{outlet_index}.pkl"),
        len(
            performance_logger_for_fifo.queue_requested_buffer_for_fifo[outlet])

    )

    add_value_to_pickle(
        os.path.join(ratio_of_occupancy_decentralized_path, f"capacity{outlet_index}.pkl"),
        outlet.current_capacity,
    )

    add_value_to_pickle(
        os.path.join(ensured_decentralized_path, f"ensured{outlet_index}.pkl"),

    len(
        performance_logger_for_fifo.queue_ensured_buffer_for_fifo[outlet])
    )



    add_value_to_pickle(
        os.path.join(waiting_buffer_length_path, f"waiting_buffer_length{outlet_index}.pkl"),
        len(
            performance_logger_for_fifo.queue_waiting_requests_in_buffer_for_fifo[outlet])
        ,
    )
    add_value_to_pickle(
        os.path.join(timed_out_length_path, f"timed_out_length{outlet_index}.pkl"),
        outlet.dqn.environment.state.timed_out_length,
    )

    add_value_to_pickle(
        os.path.join(from_waiting_to_serv_length_path, f"from_waiting_to_serv_length{outlet_index}.pkl"),
        outlet.dqn.environment.state.from_waiting_to_serv_length,
    )

    add_value_to_pickle(
        os.path.join(timed_out_requests_over_the_simulation_path, f"timed_out_requests_over_the_simulation{outlet_index}.pkl"),
        outlet.dqn.environment.state.time_out_requests_over_simulation,
    )

    add_value_to_pickle(
        os.path.join(from_wait_to_serve_requests_over_the_simulation_path, f"from_wait_to_serve_requests_over_the_simulation{outlet_index}.pkl"),
        outlet.dqn.environment.state.from_wait_to_serve_over_simulation,
    )

    add_value_to_pickle(
        os.path.join(wasting_req_length_path, f"wasting_req_length{outlet_index}.pkl"),
        len(
            performance_logger_for_fifo.queue_wasted_req_buffer_for_fifo[outlet]),
    )
    add_value_to_pickle(
        os.path.join(generated_requests_over_simulation_path, f"generated_requests_over_simulation{outlet_index}.pkl"),
        len(performance_logger_for_fifo.generated_requests_over_simulation[outlet]),
    )

    add_value_to_pickle(
        os.path.join(delay_time_path, f"delay_time{outlet_index}.pkl"),
        outlet.dqn.environment.state.delay_time,
    )


