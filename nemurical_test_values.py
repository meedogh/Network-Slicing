import numpy as np
import csv

import pandas as pd
import matplotlib.pyplot as plt

path = 'C://Users//Windows dunya//PycharmProjects//pythonProject//my_reward_with_failure_heuristic//5G_small_time_out_add_flag_small_state_my_reward_failure_test_heuristic.csv'
path2 = 'C://Users//Windows dunya//PycharmProjects//pythonProject//my_reward_with_failure_RL//5G_small_time_out_rl_add_flag_small_state_my_reward_failure_testalloutlets.csv'

# Create empty lists for each column
accepted, served, wasting, wait_to_serve, time_out, generated_requests, delayed = [], [], [], [], [], [], []

generated = []

df2 = pd.read_csv(path2)
generated = df2['generated_requests_over_simulation']
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

# Convert the lists to 32-bit integers
accepted = [np.int32(value) if pd.notna(value) else 0 for value in accepted]
served = [np.int32(value) if pd.notna(value) else 0 for value in served]
wasting = [np.int32(value) if pd.notna(value) else 0 for value in wasting]
wait_to_serve = [np.int32(value) if pd.notna(value) else 0 for value in wait_to_serve]
time_out = [np.int32(value) if pd.notna(value) else 0 for value in time_out]
generated_requests = [np.int32(value) if pd.notna(value) else 0 for value in generated_requests]
delayed = [np.int32(value) if pd.notna(value) else 0 for value in delayed]
generated = [np.int32(value) if pd.notna(value) else 0 for value in generated]
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
    index_of_end_day_one = indices[-1]
index_of_end_day_two = len(accepted) + 1
print(index_of_end_day_one , " ", index_of_end_day_two)

number_of_accepted_requests_day_one = accepted[index_of_end_day_one-2]
number_of_generated_regests_day_one = generated[index_of_end_day_one-5]
number_of_served_requests_day_one = served[index_of_end_day_one-2]
number_of_timed_out_requests_day_one = time_out[index_of_end_day_one-3]
number_of_wasting_requests_day_one = wasting[index_of_end_day_one-2]
number_of_requests_moved_from_wait_buffer_to_serve_day_one = wait_to_serve[index_of_end_day_one-3]

print(number_of_accepted_requests_day_one, " ",number_of_generated_regests_day_one , " ",number_of_served_requests_day_one , " ",
      number_of_timed_out_requests_day_one , "  ",number_of_wasting_requests_day_one , " ", number_of_requests_moved_from_wait_buffer_to_serve_day_one)


number_of_accepted_requests_day_two = accepted[index_of_end_day_two-2]
number_of_generated_regests_day_two = generated[index_of_end_day_two-2]
number_of_served_requests_day_two = served[index_of_end_day_two-2]
number_of_timed_out_requests_day_two = time_out[index_of_end_day_two-2]
number_of_wasting_requests_day_two = wasting[index_of_end_day_two-2]
number_of_requests_moved_from_wait_buffer_to_serve_day_two = wait_to_serve[index_of_end_day_two-3]

print(number_of_accepted_requests_day_two, " ",number_of_generated_regests_day_two , " ",number_of_served_requests_day_two , " ",
      number_of_timed_out_requests_day_two , "  ",number_of_wasting_requests_day_two , " ", number_of_requests_moved_from_wait_buffer_to_serve_day_two)
if number_of_requests_moved_from_wait_buffer_to_serve_day_one!=0:
    average_delayed_time_day_one = sum(delayed)/(number_of_requests_moved_from_wait_buffer_to_serve_day_one)
else :
    average_delayed_time_day_one = 0.0
if number_of_requests_moved_from_wait_buffer_to_serve_day_two!=0:
    average_delayed_time_day_two = sum(delayed)/(number_of_requests_moved_from_wait_buffer_to_serve_day_two)
else:
    average_delayed_time_day_two = 0.0
data_1={'Metrics': [ 'RequestsMovedFromWaitBufferToServe', 'AverageDelayed'],
'Day One': [
                number_of_requests_moved_from_wait_buffer_to_serve_day_one,

                average_delayed_time_day_one]
        }
data_2={
'Metrics': [ 'RequestsMovedFromWaitBufferToServe', 'AverageDelayed'],
'Day Two': [
                number_of_requests_moved_from_wait_buffer_to_serve_day_two,


                average_delayed_time_day_two]


}

df = pd.DataFrame(data_1)
df.to_csv('heuristic_5G//5G_heuristic_data_delay_day_one.csv', index=False)


df = pd.DataFrame(data_2)
df.to_csv('heuristic_5G//5G_heuristic_data_delay_day_two.csv', index=False)
# Create a dictionary with your variables
data_vis = {
    'Metrics': ['AcceptedRequests', 'GeneratedRequests', 'ServedRequests', 'TimedOutRequests',
                 '   RequestsMovedFromWaitBufferToServe'],
    'Day One': [number_of_accepted_requests_day_one,
                number_of_generated_regests_day_one,
                number_of_served_requests_day_one,
                number_of_timed_out_requests_day_one,
                number_of_requests_moved_from_wait_buffer_to_serve_day_one]
}

data2_vis = {
    'Metrics': ['AcceptedRequests', 'GeneratedRequests', 'ServedRequests', 'TimedOutRequests',
                 '   RequestsMovedFromWaitBufferToServe'],
    'Day Two': [number_of_accepted_requests_day_two,
                number_of_generated_regests_day_two,
                number_of_served_requests_day_two,
                number_of_timed_out_requests_day_two,
                number_of_requests_moved_from_wait_buffer_to_serve_day_two]
}


df = pd.DataFrame(data_vis)
df.to_csv('heuristic_5G//5G_heuristic_data_day_one.csv', index=False)
# Create a bar plot of the data
plt.figure(figsize=(10, 6))
plt.bar(df['Metrics'], df['Day One'])
plt.xlabel('Metrics', fontsize=12)  # Adjust the font size as needed
plt.ylabel('Values', fontsize=12)   # Adjust the font size as needed
plt.title('Metrics for Day One', fontsize=12)  # Adjust the font size as needed

# Rotate the x-axis labels for better visibility if needed
plt.xticks(rotation=0, fontsize=6)  # Adjust the font size as needed

# Save the plot as an SVG file
plt.savefig('heuristic_5G//5G_heuristic_data_day_one.svg', format='svg', bbox_inches='tight')

# Create a DataFrame from the dictionary
df = pd.DataFrame(data2_vis)
df.to_csv('heuristic_5G//5G_heuristic_data_day_two.csv', index=False)
# Create a bar plot of the data
plt.figure(figsize=(10, 6))
plt.bar(df['Metrics'], df['Day Two'])
plt.xlabel('Metrics', fontsize=12)  # Adjust the font size as needed
plt.ylabel('Values', fontsize=12)   # Adjust the font size as needed
plt.title('Metrics for Day Two', fontsize=12)  # Adjust the font size as needed

# Rotate the x-axis labels for better visibility if needed
plt.xticks(rotation=0, fontsize=6)  # Adjust the font size as needed

# Save the plot as an SVG file
plt.savefig('heuristic_5G//5G_heuristic_data_day_two.svg', format='svg', bbox_inches='tight')

