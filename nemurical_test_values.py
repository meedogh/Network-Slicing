import numpy as np
import csv

import pandas as pd

path = 'C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//wifi_action_req_add_wasting_buffer_rl_test1.csv'

# Create empty lists for each column
accepted, served, wasting, wait_to_serve, time_out, generated_requests, delayed = [], [], [], [], [], [], []

# Read the CSV file into a DataFrame
df = pd.read_csv(path)

# Extract the columns using the column names
accepted = df['accepted'].tolist()
served = df['served'].tolist()
wasting = df['wasting'].tolist()
wait_to_serve = df['from_wait_to_serve'].tolist()
time_out = df['time_out'].tolist()
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