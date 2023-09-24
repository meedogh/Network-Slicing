import os
import pickle
import sys

outlet_num = 0
results_dir = os.path.join(sys.path[0],f"action_each_single_request_reward_method4_add_init_10_11_12_no_protrization_less_failure//reward_accumilated_decentralize//accu_reward{outlet_num}.pkl")
# filename  = f"C://Users//Windows dunya//Downloads//action_each_single_request_reward2_method2_repeat_periods_each_episode_retrain_buffer_percentage_small_time_out_add_flag_small_state_my_reward_failure//reward_accumilated_decentralize//accu_reward{outlet_num}.pkl"

deque = []
with open(results_dir, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            deque.append(loaded_value)
    except EOFError:
        pass




print(len(deque))
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
window_size = 16
result = rolling_average(deque, window_size)
print(len(deque))
x_values = [i for i in range(len(result))]  # Adjust x-axis values

plt.plot(x_values, result, label=f'accu_reward_wifi')
plt.xlabel('episode')
plt.ylabel('accu_reward_wifi')
plt.legend()
plt.title(f'Rolling Average Plot (window={window_size})')
plt.grid(True)
plt.savefig('accu_reward_wifi.svg', format='svg')
plt.show()
