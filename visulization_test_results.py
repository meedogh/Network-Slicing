import numpy as np
import csv

import pandas as pd
import matplotlib.pyplot as plt

path = 'C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//3G_action_req_add_wasting_buffer_rl_test1.csv'

# Create empty lists for each column
accepted, served, wasting, wait_to_serve, time_out, generated_requests, delayed = [], [], [], [], [], [], []

# Read the CSV file into a DataFrame
df = pd.read_csv(path)

# Extract the columns using the column names
accepted = df['accepted'].tolist()
served = df['served'].tolist()
wasting = df['wasting'].tolist()
wait_to_serve = df['wait_to_serve_over_simulation'].tolist()
time_out = df['timed_out_over_simulation'].tolist()
generated_requests = df['generated_requests_over_simulation'].tolist()
delayed = df['delay_time'].tolist()
waiting_buffer=df['waiting_buffer_length'].tolist()

# Convert the lists to 32-bit integers
accepted = [np.int32(value) if pd.notna(value) else 0 for value in accepted]
served = [np.int32(value) if pd.notna(value) else 0 for value in served]
wasting = [np.int32(value) if pd.notna(value) else 0 for value in wasting]
wait_to_serve = [np.int32(value) if pd.notna(value) else 0 for value in wait_to_serve]
time_out = [np.int32(value) if pd.notna(value) else 0 for value in time_out]
generated_requests = [np.int32(value) if pd.notna(value) else 0 for value in generated_requests]
delayed = [np.int32(value) if pd.notna(value) else 0 for value in delayed]

print(len(accepted))
print(len(served))
print(len(wait_to_serve))
print(len(wasting))
print(len(generated_requests))
print(len(delayed))
print(len(time_out))

# Rest of your code...


indices = [index for index, value in enumerate(accepted) if value == 1]
index_of_end_day_one = 0
if indices:
    index_of_end_day_one = indices[-1] + 1
index_of_end_day_two = len(accepted) + 1
print(index_of_end_day_one , " ", index_of_end_day_two)

number_of_accepted_requests_day_one = accepted[index_of_end_day_one-2]
number_of_generated_regests_day_one = generated_requests[index_of_end_day_one-2]
number_of_served_requests_day_one = served[index_of_end_day_one-2]
number_of_timed_out_requests_day_one = time_out[index_of_end_day_one-2]
number_of_wasting_requests_day_one = wasting[index_of_end_day_one-2]
number_of_requests_moved_from_wait_buffer_to_serve_day_one = wait_to_serve[index_of_end_day_one-2]

print(number_of_accepted_requests_day_one, " ",number_of_generated_regests_day_one , " ",number_of_served_requests_day_one , " ",
      number_of_timed_out_requests_day_one , "  ",number_of_wasting_requests_day_one , " ", number_of_requests_moved_from_wait_buffer_to_serve_day_one)


number_of_accepted_requests_day_two = accepted[index_of_end_day_two-2]
number_of_generated_regests_day_two = generated_requests[index_of_end_day_two-2]
number_of_served_requests_day_two = served[index_of_end_day_two-2]
number_of_timed_out_requests_day_two = time_out[index_of_end_day_two-2]
number_of_wasting_requests_day_two = wasting[index_of_end_day_two-2]
number_of_requests_moved_from_wait_buffer_to_serve_day_two = wait_to_serve[index_of_end_day_two-2]

print(number_of_accepted_requests_day_two, " ",number_of_generated_regests_day_two , " ",number_of_served_requests_day_two , " ",
      number_of_timed_out_requests_day_two , "  ",number_of_wasting_requests_day_two , " ", number_of_requests_moved_from_wait_buffer_to_serve_day_two)


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
window_size = 1
waiting_buffer_day_one = waiting_buffer[:index_of_end_day_one-2]
waiting_buffer_day_two = waiting_buffer[index_of_end_day_one-2:index_of_end_day_two]

print(waiting_buffer_day_two)
print(len(waiting_buffer_day_two))
result = rolling_average(waiting_buffer_day_two, window_size)
# Create a list of values for the y-axis
# y_values = [10, 20, 30, 40, 50]

# Create x-values (optional, if you want to specify x-coordinates)
x_values = [i for i in range(len(waiting_buffer_day_two))]

# Create the plot
plt.plot(x_values, result)

# Add labels and a title
plt.xlabel('steps')
plt.ylabel('length of waited buffer')
plt.title('waiting_buffer_for_wifi , Day Two')
plt.savefig('waiting_buffer_length_day_two.svg', format='svg')

# Show the plot (or save it to a file using plt.savefig('filename.png'))
plt.show()

