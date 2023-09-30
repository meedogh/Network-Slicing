import itertools
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

fig = plt.figure(num=1, clear=True)
ax = fig.add_subplot(1, 1, 1, projection='3d')

def build_model() -> Sequential:
    model_ = Sequential()
    model_.add(Dense(24, input_dim=4, activation='relu'))
    model_.add(Dense(24, activation='relu'))
    model_.add(Dense(2, activation='sigmoid'))
    # model_.add(Reshape((3, 3)))
    model_.compile(loss='mse',
                   optimizer=Adam(learning_rate=0.0001))
    return model_


model = build_model()
model.load_weights(
    f'{os.path.join(sys.path[0])}//action_each_single_request_reward_method4_add_init_10_11_12_less_failure_0_10_m1_100//decentralized_weights/weights_0_100.hdf5')

# Calculate Q-values for each (x1, x2) pair (replace this with your actual Q-values)
# x1_time_out = np.arange(2,11, 1)
# y1_current_capacity = 0.01
# bl = np.arange(90,100, 1)
# pa = 2.54
# (x1_time_out_, y1_current_capacity_) = np.meshgrid(x1_time_out, y1_current_capacity)
# x1_flattened = x1_time_out_.flatten()
# y1_flattened = bl.flatten()
#
# states1 = []
# number_of_points_in_mesh = len(x1_flattened)
# for index in range(number_of_points_in_mesh):
#     states1.append([x1_flattened[index], y1_current_capacity, pa, y1_flattened[index]])
#
# action1 = []
# for i in range(number_of_points_in_mesh):
#     states1[i] = np.array(states1[i]).reshape([1, np.array(states1[i]).shape[0]])
#     print("action model : ", np.argmax(model.predict(states1[i])))
#     action1.append(np.argmax(model.predict(states1[i])))
#
# action1 = np.array(action1).reshape(x1_time_out_.shape[0], y1_current_capacity_.shape[1])


#
x2_buffer_length = np.arange(95, 100, 0.5)
y2_current_capacity = np.arange(0.05, 2.55, 0.5)
tout = 2
pa2 = 10

(x2_buffer_length_, y2_current_capacity_) = np.meshgrid(x2_buffer_length, y2_current_capacity)
x2_flattened = x2_buffer_length_.flatten()
y2_flattened = y2_current_capacity_.flatten()

states2 = []
number_of_points_in_mesh = len(x2_flattened)
for index in range(number_of_points_in_mesh):
    states2.append([tout,y2_flattened[index],pa2,x2_flattened[index]])

action2 = []
for i in range(number_of_points_in_mesh):
    states2[i] = np.array(states2[i]).reshape([1, np.array(states2[i]).shape[0]])
    print("action model : ", np.argmax(model.predict(states2[i])))
    action2.append(np.argmax(model.predict(states2[i])))

action2 = np.array(action2).reshape(x2_buffer_length_.shape[0], x2_buffer_length_.shape[1])
#
# x3_power_allocation = np.arange(0.5, 5.5, 0.5)
# y3_current_capacity = np.arange(80, 90, 1)
# tout3 = 80
# bl3 = 1
#
# (x3_power_allocation_, y3_current_capacity_) = np.meshgrid(x3_power_allocation, y3_current_capacity)
# x3_flattened = x3_power_allocation_.flatten()
# y3_flattened = y3_current_capacity_.flatten()
# states3 = []
# number_of_points_in_mesh = len(x3_flattened)
# for index in range(number_of_points_in_mesh):
#     states3.append([tout3,y3_flattened[index],x3_flattened[index],bl3])
#
# action3 = []
# for i in range(number_of_points_in_mesh):
#     states3[i] = np.array(states3[i]).reshape([1, np.array(states3[i]).shape[0]])
#     print("action model : ", np.argmax(model.predict(states3[i])))
#     action3.append(np.argmax(model.predict(states3[i])))
#
# action3 = np.array(action3).reshape(x3_power_allocation_.shape[0], x3_power_allocation_.shape[1])



# ax.plot_surface(x1_time_out_, y1_current_capacity_, action1, cmap='coolwarm')
# ax.set(xlabel='request time out%', ylabel='tower current capacity%', zlabel='z', title='z = argmax(qvalue)')
# plt.savefig("plot(TO,CC).svg", format="svg")
# plt.show()

ax.plot_surface(x2_buffer_length_, y2_current_capacity_, action2, cmap='coolwarm')
ax.set(xlabel='buffer length%', ylabel='tower current capacity%', zlabel='z', title='z = argmax(qvalue)')
plt.savefig("plot(BL,CC).svg", format="svg")
plt.show()
#
# ax.plot_surface(x3_power_allocation_, y3_current_capacity_, action3, cmap='coolwarm')
# ax.set(xlabel='request power allocation%', ylabel='tower current capacity%', zlabel='z', title='z = argmax(qvalue)')
# plt.savefig("plot(PA,CC).svg", format="svg")
# plt.show()