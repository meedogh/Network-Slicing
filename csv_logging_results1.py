import os
import pickle
import sys

import pandas as pd

# outlet outlet_number [0,1,2,3]
outlet_name = ['wifi', '3G', '4G', '5G']
method_name = ['rl', 'fifo', 'heuristic']
outlet_num = 0

results_dir_train_results = f"{os.path.join(sys.path[0])}/action_each_single_request_reward_method4_add_init_10_11_12_less_failure_0_10_m1_100_test"
results_dir_test_results = f"{os.path.join(sys.path[0])}/action_each_single_request_reward_method4_testalloutlets"

reward = os.path.join(results_dir_train_results, f"reward_decentralized/reward{outlet_num}.pkl")
action = os.path.join(results_dir_train_results, f"action_decentralized/action{outlet_num}.pkl")
requested = os.path.join(results_dir_train_results, f"requested_decentralized/requested{outlet_num}.pkl")
ensured = os.path.join(results_dir_train_results, f"ensured_decentralized/ensured{outlet_num}.pkl")
supported = os.path.join(results_dir_train_results,
                         f"supported_service_decentralized/supported_services{outlet_num}.pkl")
capacity = os.path.join(results_dir_train_results, f"ratio_of_occupancy_decentralized/capacity{outlet_num}.pkl")
waiting_buffer_length = os.path.join(results_dir_train_results,
                                     f"waiting_buffer_length/waiting_buffer_length{outlet_num}.pkl")
timed_out_requests = os.path.join(results_dir_train_results, f"timed_out_length/timed_out_length{outlet_num}.pkl")
from_wait_to_serve = os.path.join(results_dir_train_results,
                                  f"from_waiting_to_serv_length/from_waiting_to_serv_length{outlet_num}.pkl")
wasting = os.path.join(results_dir_train_results, f"wasting_req_length/wasting_req_length{outlet_num}.pkl")
from_wait_to_serve_over_simulation = os.path.join(results_dir_train_results,
                                                  f"from_wait_to_serve_requests_over_the_simulation/from_wait_to_serve_requests_over_the_simulation{outlet_num}.pkl")
timed_out_requests_over_simulation = os.path.join(results_dir_train_results,
                                                  f"timed_out_requests_over_the_simulation/timed_out_requests_over_the_simulation{outlet_num}.pkl")
generated_requests_over_simulation = os.path.join(results_dir_train_results,
                                                  f"generated_requests_over_simulation/generated_requests_over_simulation{outlet_num}.pkl")
print(generated_requests_over_simulation)
delay_time_path = os.path.join(results_dir_train_results, f"delay_time/delay_time{outlet_num}.pkl")
number_of_abort_requests_over_the_simulation_path = os.path.join(results_dir_train_results,
                                                                 f"number_of_abort_requests_over_the_simulation/number_of_abort_requests_over_the_simulation{outlet_num}.pkl")
number_of_rejected_requests_over_simulation_path = os.path.join(results_dir_train_results,
                                                                f"number_of_rejected_requests_over_simulation/number_of_rejected_requests_over_simulation{outlet_num}.pkl")
sum_of_cost_of_all_rejected_requests_path = os.path.join(results_dir_train_results,
                                                         f"sum_of_cost_of_all_rejected_requests/sum_of_cost_of_all_rejected_requests{outlet_num}.pkl")
abort_req = []
rejected_over_simulation = []
cost_of_rejected_requests = []
delay_time = []
timed_out_over_simulation = []
wait_to_serve_over_simulation = []
timed_out = []
from_wait_t_serve = []
generated_requests_over_simulation_list = []
cap = []
mcap = []
av_cap = []
rew = []
act = []
uti = []
req = []
ens = []
sup = []
pow_ = []
occu_ = []
wast = []
waiting_buffer = []

with open(number_of_abort_requests_over_the_simulation_path, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            abort_req.append(loaded_value)
    except EOFError:
        pass

with open(number_of_rejected_requests_over_simulation_path, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            rejected_over_simulation.append(loaded_value)
    except EOFError:
        pass

with open(sum_of_cost_of_all_rejected_requests_path, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            cost_of_rejected_requests.append(loaded_value)
    except EOFError:
        pass
with open(delay_time_path, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            delay_time.append(loaded_value)
    except EOFError:
        pass

with open(timed_out_requests_over_simulation, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            timed_out_over_simulation.append(loaded_value)
    except EOFError:
        pass

with open(from_wait_to_serve_over_simulation, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            wait_to_serve_over_simulation.append(loaded_value)
    except EOFError:
        pass

with open(wasting, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            wast.append(loaded_value)
    except EOFError:
        pass

with open(timed_out_requests, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            timed_out.append(loaded_value)
    except EOFError:
        pass

with open(from_wait_to_serve, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            from_wait_t_serve.append(loaded_value)
    except EOFError:
        pass

with open(waiting_buffer_length, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            waiting_buffer.append(loaded_value)
    except EOFError:
        pass

with open(reward, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            rew.append(loaded_value)
    except EOFError:
        pass

with open(action, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            act.append(loaded_value)
    except EOFError:
        pass

with open(requested, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            req.append(loaded_value)
    except EOFError:
        pass
with open(ensured, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            ens.append(loaded_value)
    except EOFError:
        pass
with open(supported, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            sup.append(loaded_value)
    except EOFError:
        pass

with open(capacity, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            cap.append(loaded_value)
    except EOFError:
        pass
with open(generated_requests_over_simulation, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            generated_requests_over_simulation_list.append(loaded_value)
    except EOFError:
        pass

columns = {}

columns['capacity'] = cap
columns["action"] = act
columns["reward"] = rew
columns["accepted"] = req
columns["served"] = ens
columns['waiting_buffer_length'] = waiting_buffer
columns['time_out'] = timed_out
columns['from_wait_to_serve'] = from_wait_t_serve
columns["supported"] = sup
columns["wasting"] = wast
columns["wait_to_serve_over_simulation"] = wait_to_serve_over_simulation
columns["timed_out_over_simulation"] = timed_out_over_simulation
columns['generated_requests_over_simulation'] = generated_requests_over_simulation_list
columns['delay_time'] = delay_time
columns['cost of rejected requests'] = cost_of_rejected_requests
columns['rejected over simulation'] = rejected_over_simulation
columns['aborted requests'] = abort_req
data = list(
    zip(
        # columns["occupancy"],
        columns['capacity'],
        # columns['max capacity'],
        # columns["serving ratio"],
        columns["action"],
        columns["reward"],
        columns["accepted"],
        columns["served"],
        columns['waiting_buffer_length'],
        columns['time_out'],
        columns['from_wait_to_serve'],
        columns["supported"],
        columns["wasting"],
        columns["wait_to_serve_over_simulation"],
        columns["timed_out_over_simulation"],
        columns['generated_requests_over_simulation'],
        columns['delay_time'],
        columns['cost of rejected requests'],
        columns['rejected over simulation'],
        columns['aborted requests'],
    )
)

df = pd.DataFrame(data=data, columns=list(columns.keys()))

df.to_csv(f"{outlet_name[outlet_num]}_10_11_12_train_10_0_m1_test_{method_name[outlet_num]}.csv",
          index=False)
