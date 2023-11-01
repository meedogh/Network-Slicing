import pickle

path1 = "C:/Users/Windows dunya/PycharmProjects/pythonProject/Network-Slicing/throughputdata_for_grid_search(0.1,-0.2,-0.1)"
path2 ="C:/Users/Windows dunya/PycharmProjects/pythonProject/Network-Slicing/throughputdata_for_grid_search(0.1,-0.6,-0.5)"
path3 ="C:/Users/Windows dunya/PycharmProjects/pythonProject/Network-Slicing/throughputdata_for_grid_search(0.1,-1,-0.5)"
path4 ="C:/Users/Windows dunya/PycharmProjects/pythonProject/Network-Slicing/throughputdata_for_grid_search(0.2,-0.2,-0.1)"
path5  ="C:/Users/Windows dunya/PycharmProjects/pythonProject/Network-Slicing/throughputdata_for_grid_search(0.5,-1,-0.5)"

data1 = []
data2 = []
data3 = []
data4 = []
data5 = []
# Open the pickle file in read mode
with open(path1, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            data1.append(loaded_value)
    except EOFError:
        pass

with open(path2, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            data2.append(loaded_value)
    except EOFError:
        pass

with open(path3, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            data3.append(loaded_value)
    except EOFError:
        pass

with open(path4, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            data4.append(loaded_value)
    except EOFError:
        pass

with open(path5, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            data5.append(loaded_value)
    except EOFError:
        pass

sum_of_acc = 0
sum_of_serv = 0


for d1 in data1:
    # print("acc : ",d1[0])
    # print("ser : ",d1[1])
    sum_of_acc+=d1[0]
    sum_of_serv+=d1[1]
if sum_of_acc!=0:
    print("data_for_grid_search(0.1,-0.2,-0.1) : ", sum_of_serv/64311 )
sum_of_acc = 0
sum_of_serv = 0

for d2 in data2:
    # print("acc : ", d2[0])
    # print("ser : ", d2[1])
    sum_of_acc += d2[0]
    sum_of_serv += d2[1]
if sum_of_acc!=0:
    print("data_for_grid_search(0.1,-0.6,-0.5) : ", sum_of_serv/64115 )
sum_of_acc = 0
sum_of_serv = 0

for d3 in data3:
    # print("acc : ", d3[0])
    # print("ser : ", d3[1])
    sum_of_acc += d3[0]
    sum_of_serv += d3[1]
if sum_of_acc!=0:
    print("data_for_grid_search(0.1,-1,-0.5) : ", sum_of_serv/66358 )
sum_of_acc = 0
sum_of_serv = 0

for d4 in data4:
    # print("acc : ", d4[0])
    # print("ser : ", d4[1])
    sum_of_acc += d4[0]
    sum_of_serv += d4[1]
if sum_of_acc!=0:
    print("data_for_grid_search(0.2,-0.2,-0.1) : ", sum_of_serv/65254)

sum_of_acc = 0
sum_of_serv = 0

for d5 in data5:
    # print("acc : ", d5[0])
    # print("ser : ", d5[1])
    sum_of_acc += d5[0]
    sum_of_serv += d5[1]
if sum_of_acc != 0:
    print("data_for_grid_search(0.5,-1,-0.5) : ", sum_of_serv/66654)
print(data5)