import itertools
import os
import sys

import matplotlib
import matplotlib.pyplot as plt
import  numpy as np
import pickle as pk

from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

fig = plt.figure(num=1, clear=True)
ax = fig.add_subplot(1, 1, 1, projection='3d')



file_serve = f"{os.path.join(sys.path[0])}//served_state.pkl"
serve = []
with open(file_serve, 'rb') as file:
    try:
        while True:
            loaded_value = pk.load(file)
            serve.append(loaded_value)
    except EOFError:
        pass



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
    f'{os.path.join(sys.path[0])}//action_each_single_request_reward_method4//decentralized_weights/weights_0_140.hdf5')

# Calculate Q-values for each (x1, x2) pair (replace this with your actual Q-values)
x = np.arange(80,90, 0.5)
y = np.arange(85,105,0.5)

# x = np.arange(1, 10, 2)
# y = np.arange(80,90,2)
(x1, y1) = np.meshgrid(x,y)
print(x1.shape)
print(y1.shape)
print(x1)
print(y1)
x_flattened =  x1.flatten()
# print(x_flattened)
y_flattened =  y1.flatten()
# print(y_flattened)
states = []

buffer_length = 20
flag_value = 0

# print(len(x_flattened))
# permutations = list(itertools.product(x_flattened, y_flattened))
# x_permutations = []
# y_permutations = []
number_of_points_in_mesh = len(x_flattened)
for index in range(number_of_points_in_mesh):
    states.append([x_flattened[index],y_flattened[index],buffer_length,flag_value])


action = []

for i in range(number_of_points_in_mesh):
    states[i] = np.array(states[i]).reshape([1, np.array(states[i]).shape[0]])
    print("action model : ",np.argmax(model.predict(states[i])))
    action.append(np.argmax(model.predict(states[i])))

print(action)
action = np.array(action).reshape(x1.shape[0],x1.shape[1])
print(action)
# # x_flattened = np.array(x_flattened).reshape(np.array(x_flattened).shape[0],1)
# # y_flattened = np.array(y_flattened).reshape(np.array(y_flattened).shape[0],1)
#



ax.plot_surface(x1, y1, action , cmap='coolwarm')
ax.set(xlabel='request power allocation%', ylabel='buffer length%', zlabel='z', title='z = argmax(qvalue)')


plt.savefig("plot(PA,BL).svg", format="svg")
plt.show()