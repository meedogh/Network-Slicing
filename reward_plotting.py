import os
import pickle
import sys


outlet_num = 0
# results_dir = os.path.join(sys.path[0],f"run_rl_just_on_rush_hours_lr_0.001//reward_accumilated_decentralize//accu_reward{outlet_num}.pkl")
deque = []
epsilon_list = []
for i in range(91,93):
    epsilon = 0.95
    results_dir = os.path.join(sys.path[0],f"run_rl_just_on_rush_hours_lr_0.001_{i}//reward_accumilated_decentralize//accu_reward{outlet_num}.pkl")

        # filename  = f"C://Users//Windows dunya//Downloads//action_each_single_request_reward2_method2_repeat_periods_each_episode_retrain_buffer_percentage_small_time_out_add_flag_small_state_my_reward_failure//reward_accumilated_decentralize//accu_reward{outlet_num}.pkl"
    
    with open(results_dir, 'rb') as file:
        try:
            while True:
                # print("EPIII", epsilon)
                loaded_value = pickle.load(file)
                
                deque.append(loaded_value)
                epsilon -= epsilon * 0.0025
                epsilon_list.append(epsilon)
        except EOFError:
            continue
# for i in range(1,6):
#     # if i <= 43:
#     #     results_dir = os.path.join(sys.path[0],f"d:\\NS//run_rl_just_on_rush_hours_lr_0.001_{i}//reward_accumilated_decentralize//accu_reward{outlet_num}.pkl")
#     # else:
#     results_dir = os.path.join(sys.path[0],f"d:\\NS//run_rl_just_on_rush_hours_lr_0.001_ep_greedy{i}//reward_accumilated_decentralize//accu_reward{outlet_num}.pkl")

#     # filename  = f"C://Users//Windows dunya//Downloads//action_each_single_request_reward2_method2_repeat_periods_each_episode_retrain_buffer_percentage_small_time_out_add_flag_small_state_my_reward_failure//reward_accumilated_decentralize//accu_reward{outlet_num}.pkl"

#     with open(results_dir, 'rb') as file:
#         try:
#             while True:
#                 loaded_value = pickle.load(file)
#                 deque.append(loaded_value)
#         except EOFError:
#             pass

        # with open(results_dir2, 'rb') as file:
        #     try:
        #         while True:
        #             loaded_value = pickle.load(file)
        #             deque.append(loaded_value)
        #     except EOFError:
        #         pass


        # with open(results_dir3, 'rb') as file:
        #     try:
        #         while True:
        #             loaded_value = pickle.load(file)
        #             deque.append(loaded_value)
        #     except EOFError:
        #         pass

        # with open(results_dir4, 'rb') as file:
        #     try:
        #         while True:
        #             loaded_value = pickle.load(file)
        #             deque.append(loaded_value)
        #     except EOFError:
        #         pass

        # with open(results_dir5, 'rb') as file:
        #     try:
        #         while True:
        #             loaded_value = pickle.load(file)
        #             deque.append(loaded_value)
        #     except EOFError:
        #         pass

        # with open(results_dir6, 'rb') as file:
        #     try:
        #         while True:
        #             loaded_value = pickle.load(file)
        #             deque.append(loaded_value)
        #     except EOFError:
        #         pass

        # with open(results_dir7, 'rb') as file:
        #     try:
        #         while True:
        #             loaded_value = pickle.load(file)
        #             deque.append(loaded_value)
        #     except EOFError:
        #         pass


        # with open(results_dir8, 'rb') as file:
        #     try:
        #         while True:
        #             loaded_value = pickle.load(file)
        #             deque.append(loaded_value)
        #     except EOFError:
        #         pass


        # with open(results_dir9, 'rb') as file:
        #     try:
        #         while True:
        #             loaded_value = pickle.load(file)
        #             deque.append(loaded_value)
        #     except EOFError:
        #         pass

        # with open(results_dir10, 'rb') as file:
        #     try:
        #         while True:
        #             loaded_value = pickle.load(file)
        #             deque.append(loaded_value)
        #     except EOFError:
        #         pass

print("TEST", len(deque))
for i in deque:
    print(i)
    print("\n")
print("Folder contents copied successfully.")

import numpy as np
import matplotlib.pyplot as plt

def rolling_average(data, window_size):
    # Convert the data to a NumPy array with float type
    data_array = np.array(data, dtype=np.float64)

    # Pad the data with NaN values at the beginning to maintain the length of the output
    padded_data = np.pad(data_array, (window_size-1, 0), mode='constant', constant_values=np.nan)

    # Calculate the rolling average using convolution with a window of ones
    weights = np.ones(window_size) / window_size
    rolling_avg = np.convolve(padded_data, weights, mode='valid')

    return rolling_avg

# Example usage:
window_size = 25

# Assuming you have a list named 'deque' and 'epsilon_list'
result = rolling_average(deque, window_size)
result2 = rolling_average(epsilon_list, window_size)
x_values = [i for i in range(len(result))]  # Adjust x-axis values
epsilon_values = [i for i in range(len(result2))]
plt.figure(1)
plt.plot(x_values, deque, label='Original Data', marker='o')
plt.plot(x_values, result, label=f'accu_reward_wifi')
plt.xlabel('episode')
plt.ylabel('Values')
plt.legend()
plt.title(f'Rolling Average Plot (window={window_size})')
plt.grid(True)

# Create a figure for the second plot
# plt.figure(2)
# plt.plot(epsilon_values, epsilon_list, label='Epsilon List', marker='o')
# plt.xlabel('episode')
# plt.ylabel('Values')
# plt.legend()
# plt.title('Epsilon List Plot')
# plt.grid(True)

plt.savefig('run_rl_just_on_rush_hours.svg', format='svg')
plt.show()
