import os

from Environment.utils.helpers import add_value_to_pickle
from Environment.utils.paths import *

def logging_important_info_for_testing(performance_logger,
        outlet_index,outlet,satellite ):
    if outlet_index < 4:
        # print("Outlet Spandex", outlet_index)
        # pass

        # add_value_to_pickle(
        #     os.path.join(reward_decentralized_path, f"reward{outlet_index}.pkl"),
        #     outlet.dqn.environment.reward.reward_value,
        # )

        # add_value_to_pickle(
        #     os.path.join(requested_decentralized_path, f"requested{outlet_index}.pkl"),
        #
        #         performance_logger.queue_requested_buffer[outlet],
        # )

        # add_value_to_pickle(
        #     os.path.join(ratio_of_occupancy_decentralized_path, f"capacity{outlet_index}.pkl"),
        #     outlet.current_capacity,
        # )
        #
        # add_value_to_pickle(
        #     os.path.join(ensured_decentralized_path, f"ensured{outlet_index}.pkl"),
        #
        #         performance_logger.queue_ensured_buffer[outlet],
        # )
        #
        # add_value_to_pickle(
        #     os.path.join(action_decentralized_path, f"action{outlet_index}.pkl"),
        #     outlet.dqn.agents.action.command.action_value_decentralize,
        # )
        #
        # add_value_to_pickle(
        #     os.path.join(supported_service_decentralized_path, f"supported_services{outlet_index}.pkl"),
        #     outlet.supported_services,
        # )
        #
        # add_value_to_pickle(
        #     os.path.join(waiting_buffer_length_path, f"waiting_buffer_length{outlet_index}.pkl"),
        #     outlet.dqn.environment.state.waiting_buffer_len,
        # )
        add_value_to_pickle(
            os.path.join(timed_out_length_path, f"timed_out_length{outlet_index}.pkl"),
            outlet.dqn.environment.state.timed_out_length,
        )
        #
        # add_value_to_pickle(
        #     os.path.join(from_waiting_to_serv_length_path, f"from_waiting_to_serv_length{outlet_index}.pkl"),
        #     outlet.dqn.environment.state.from_waiting_to_serv_length,
        # )
        #
        add_value_to_pickle(
            os.path.join(timed_out_requests_over_the_simulation_path, f"timed_out_requests_over_the_simulation{outlet_index}.pkl"),
            outlet.dqn.environment.state.time_out_requests_over_simulation,
        )
        #
        # add_value_to_pickle(
        #     os.path.join(from_wait_to_serve_requests_over_the_simulation_path, f"from_wait_to_serve_requests_over_the_simulation{outlet_index}.pkl"),
        #     outlet.dqn.environment.state.from_wait_to_serve_over_simulation,
        # )

        # add_value_to_pickle(
        #     os.path.join(wasting_req_length_path, f"wasting_req_length{outlet_index}.pkl"),
        #     outlet.dqn.environment.state.wasting_buffer_length,
        # )
        add_value_to_pickle(
            os.path.join(generated_requests_over_simulation_path, f"generated_requests_over_simulation{outlet_index}.pkl"),
            performance_logger.generated_requests_over_simulation,
        )
        add_value_to_pickle(
            os.path.join(served_requests_over_simulation_path, f"served_requests_{outlet_index}.pkl"),
            performance_logger.served_requests_over_simulation,
        )
        #
        add_value_to_pickle(
            os.path.join(delay_time_path, f"delay_time{outlet_index}.pkl"),
            outlet.dqn.environment.state.delay_time,
        )
        # print(outlet.dqn.environment.state.delay_time)

        add_value_to_pickle(
            os.path.join(number_of_timed_out_requests_from_algorithm_path,f"number_of_timed_out_requests_from_algorithm{outlet_index}.pkl")
            , outlet.dqn.environment.state.number_of_timed_out_requests_from_algorithm,
        )
        add_value_to_pickle(
            os.path.join(number_of_rejected_requests_over_simulation_path,f"number_of_rejected_requests_over_simulation{outlet_index}.pkl"),
            len(satellite.rejected_requests_buffer)
        )
        #
        add_value_to_pickle(
            os.path.join(sum_of_cost_of_all_rejected_requests_path,
                        f"sum_of_cost_of_all_rejected_requests{outlet_index}.pkl"),
            satellite.sum_of_costs_of_all_requests
        )
        add_value_to_pickle(
            os.path.join(number_of_abort_requests_over_the_simulation_path,
                        f"number_of_abort_requests_over_the_simulation{outlet_index}.pkl"),
            outlet.abort_requests
        )


    # def logging_user_info_for_utility():
    #     add_value_to_pickle(
    #         os.path.join(,""),
    #
    #     )