import pickle as pk

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
list_of_values = []


# Read the CSV file into a DataFrame
path = 'C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//wifi_action_req_add_wasting_buffer12.csv'

#import csv
# column_data = []
# Open the CSV file
with open(path, 'r') as file:
    reader = csv.reader(file)

    # Assuming the column you want to read is the second column (index 1)
    column_index = 5
    index_of_delay = 13
    column_data = []
    delay_column =[]

    for row in reader:
        column_data.append(row[column_index])
    # for row in reader:
    #     delay_column.append(row[index_of_delay])
# print(column_data)

delay_column = delay_column[1:]
# print(delay_column)
delay_column = [np.int32(value) for value in delay_column]

# print(sum(delay_column))
# Now, column_data contains the values from the specified column as a list
# print(column_data)

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
window_size = 200
column_data = column_data[1:]
column_data = [np.int32(value) for value in column_data]
result = rolling_average(column_data, window_size)
# Create a list of values for the y-axis
# y_values = [10, 20, 30, 40, 50]

# Create x-values (optional, if you want to specify x-coordinates)
x_values = [i for i in range(3193)]

# Create the plot
plt.plot(x_values, result)

# Add labels and a title
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')
plt.title('waiting_buffer_for_lr')
plt.savefig('waiting_buffer_for_lr.svg', format='svg')

# Show the plot (or save it to a file using plt.savefig('filename.png'))
plt.show()

