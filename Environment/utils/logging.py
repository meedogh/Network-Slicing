import os

from Environment.utils.helpers import add_value_to_pickle


def logging_important_info_for_testing(outlet_index,outlet ,reward_decentralized_path,requested_decentralized_path,ratio_of_occupancy_decentralized_path
                                       ,ensured_decentralized_path,action_decentralized_path,supported_service_decentralized_path ,waiting_buffer_length_path,timed_out_length_path, from_waiting_to_serv_length_path):

    add_value_to_pickle(
        os.path.join(reward_decentralized_path, f"reward{outlet_index}.pkl"),
        outlet.dqn.environment.reward.reward_value,
    )

    add_value_to_pickle(
        os.path.join(requested_decentralized_path, f"requested{outlet_index}.pkl"),
        outlet.dqn.environment.reward.services_requested,
    )

    add_value_to_pickle(
        os.path.join(ratio_of_occupancy_decentralized_path, f"capacity{outlet_index}.pkl"),
        outlet.current_capacity,
    )

    add_value_to_pickle(
        os.path.join(ensured_decentralized_path, f"ensured{outlet_index}.pkl"),
        outlet.dqn.environment.reward.services_ensured,
    )

    add_value_to_pickle(
        os.path.join(action_decentralized_path, f"action{outlet_index}.pkl"),
        outlet.dqn.agents.action.command.action_value_decentralize,
    )

    add_value_to_pickle(
        os.path.join(supported_service_decentralized_path, f"supported_services{outlet_index}.pkl"),
        outlet.supported_services,
    )

    add_value_to_pickle(
        os.path.join(waiting_buffer_length_path, f"waiting_buffer_length{outlet_index}.pkl"),
        outlet.dqn.environment.state.waiting_buffer_len,
    )
    add_value_to_pickle(
        os.path.join(timed_out_length_path, f"timed_out_length{outlet_index}.pkl"),
        outlet.dqn.environment.state.timed_out_length,
    )

    add_value_to_pickle(
        os.path.join(from_waiting_to_serv_length_path, f"from_waiting_to_serv_length{outlet_index}.pkl"),
        outlet.dqn.environment.state.from_waiting_to_serv_length,
    )

