import csv
import os
import re
import sys

import pandas as pd


outlet_name = ['wifi','3G','4G','5G']
method_name =  ['rl' , 'fifo' ,'heuristic']
outlet_num = 0

folders = [os.path.join(sys.path[0], f'results//{method_name[outlet_num]}_wifi'), os.path.join(sys.path[0], f'results//{method_name[outlet_num]}_3G'), os.path.join(sys.path[0], f'results//{method_name[outlet_num]}_4G'),
           os.path.join(sys.path[0], f'results//{method_name[outlet_num]}_5G')]
day_name=["day_one","day_wo"]
rows_to_extract = [
    'AcceptedRequests',
    'GeneratedRequests',
    'ServedRequests',
    'TimedOutRequests',
    'RequestsMovedFromWaitBufferToServe',
    'AverageDelayed',
    'ServingRatio',
    'overall throughput',

]

import os

outlets_name = ['wifi','3G','4G','5G']
data_day_one={f"wifi":[],f"3G":[],f"4G":[],f"5G":[]}
data_day_two={f"wifi":[],f"3G":[],f"4G":[],f"5G":[]}
for index , folder in enumerate(folders):
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        througout = 0
        sum_serving = 0
        generated = 0
        accepted = 0
        serving =0
        if os.path.isfile(item_path):
            if item_path.endswith('1.csv') and item.find("day_one") != -1:
                df = pd.read_csv(item_path, encoding='utf-8')
                data_day_one[f"{outlets_name[index]}"] = df.iloc[:, 1].tolist()
            if item_path.endswith('2.csv') and item.find("day_one") != -1:
                df = pd.read_csv(item_path, encoding='utf-8')
                data_day_one[f"{outlets_name[index]}"].append(df.iloc[:, 1].tolist()[-1])
        # if generated !=0:
        #     througout = float(sum_serving) / float(generated)
        # data_day_one[f"{outlets_name[index]}"].append(througout)
#
for index , folder in enumerate(folders):
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isfile(item_path):
            if item_path.endswith('1.csv') and item.find("day_two") != -1:
                df = pd.read_csv(item_path, encoding='utf-8')
                data_day_two[f"{outlets_name[index]}"] = df.iloc[:, 1].tolist()
            if item_path.endswith('2.csv') and item.find("day_two") != -1:
                df = pd.read_csv(item_path, encoding='utf-8')
                data_day_two[f"{outlets_name[index]}"].append(df.iloc[:, 1].tolist()[-1])
print(data_day_one)
print(data_day_two)

sum_serving = 0
througout  = 0
for key , value in data_day_one.items():
    serving = data_day_one[key][2]
    accepted = data_day_one[key][0]
    generated = data_day_one[key][1]
    serving_ratio = float(serving) / float(accepted)
    sum_serving += float(serving)
    data_day_one[key].append(serving_ratio)

througout = sum_serving/generated

for key, value in data_day_two.items():
    data_day_one[key].append(througout)

sum_serving  = 0
for key , value in data_day_two.items():
    serving = data_day_two[key][2]
    accepted = data_day_two[key][0]
    generated = data_day_two[key][1]
    serving_ratio = float(serving) / float(accepted)
    sum_serving += float(serving)
    data_day_two[key].append(serving_ratio)

througout = sum_serving/generated
for key, value in data_day_two.items():
    data_day_two[key].append(througout)

print(data_day_one)
print(data_day_two)
# Create a DataFrame from the dictionary
df = pd.DataFrame(data_day_one)

with open(f'final_results//data_day_one_{method_name[outlet_num]}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row with column names
    writer.writerow([''] + list(data_day_one.keys()))

    # Write the rows
    for i, row_name in enumerate(rows_to_extract):
        writer.writerow([row_name] + [data_day_one[column][i] for column in data_day_one.keys()])

df = pd.DataFrame(data_day_two)

with open(f'final_results//data_day_two_{method_name[outlet_num]}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row with column names
    writer.writerow([''] + list(data_day_two.keys()))

    # Write the rows
    for i, row_name in enumerate(rows_to_extract):
        writer.writerow([row_name] + [data_day_two[column][i] for column in data_day_two.keys()])
