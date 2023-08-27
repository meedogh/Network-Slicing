import numpy as np
import pandas as pd
import csv

list_of_values = []

# Read the CSV file into a DataFrame
path = 'C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//wifi_action_req_add_wasting_buffer_rl_test1.csv'

# import csv
# column_data = []
# Open the CSV file
with open(path, 'r') as file:
    reader = csv.reader(file)

    # Assuming the column you want to read is the second column (index 1)
    index_of_accepted = 3
    index_of_served = 4
    index_of_wasting = 9
    index_of_wait_to_serve = 10
    index_of_time_out = 11
    index_of_generated_requests = 12
    index_of_delayed = 13

    accepted = []
    served = []
    wasting = []
    wait_to_serve = []
    time_out = []
    generated_requests = []
    delayed = []

    for row in reader:
        accepted.append(row[index_of_accepted])
    for row in reader:
        served.append(row[index_of_served])
    for row in reader:
        wasting.append(row[index_of_wasting])
    for row in reader:
        wait_to_serve.append(row[index_of_wait_to_serve])
    for row in reader:
        time_out.append(row[index_of_time_out])
    for row in reader:
        generated_requests.append(row[index_of_generated_requests])
    for row in reader:
        delayed.append(row[index_of_delayed])

accepted = accepted[1:]
served = served[1:]
wasting = wasting[1:]
wait_to_serve = wait_to_serve[1:]
time_out = time_out[1:]
generated_requests = generated_requests[1:]
delayed = delayed[1:]
accepted = accepted[1:]

accepted = [np.int32(value) for value in accepted]
served = [np.int32(value) for value in served]
wasting = [np.int32(value) for value in wasting]
wait_to_serve = [np.int32(value) for value in wait_to_serve]
time_out = [np.int32(value) for value in time_out]
generated_requests = [np.int32(value) for value in generated_requests]
delayed = [np.int32(value) for value in delayed]
accepted = [np.int32(value) for value in accepted]

indices = [index for index, value in enumerate(accepted) if value == 1]
index_of_end_day_one = 0
if indices:
    index_of_end_day_one = indices[-1]
index_of_end_day_two = len(accepted) - 1
