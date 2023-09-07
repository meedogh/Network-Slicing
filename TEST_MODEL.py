import matplotlib.pyplot as plt
import  numpy as np
import pickle as pk

from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

fig = plt.figure(num=1, clear=True)
ax = fig.add_subplot(1, 1, 1, projection='3d')



file_serve = "C://Users//Windows dunya//PycharmProjects//pythonProject//the final results exp//served_state.pkl"
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
    'C://Users//Windows dunya//Downloads//action_each_single_request_reward2_method2_repeat_periods_each_episode_retrain_buffer_percentage_small_time_out_add_flag_small_state_my_reward_failure//decentralized_weights/weights_0_140.hdf5')

# Calculate Q-values for each (x1, x2) pair (replace this with your actual Q-values)
x = np.arange(1, 100, 10)
y = np.arange(1, 50, 10)

# x = np.arange(1, 10, 2)
# y = np.arange(80,90,2)
(x1, y1) = np.meshgrid(x,y )

states = []
number_of_points_in_mesh = 5
buffer_length = 20
flag_value = 0
for i in range(number_of_points_in_mesh):
    states.append([x[i],y[i], buffer_length,flag_value])

action = []
for i in range(number_of_points_in_mesh):
    states[i] = np.array(states[i]).reshape([1, np.array(states[i]).shape[0]])
    action.append(np.argmax(model.predict(states[i])))

action = np.array(action).reshape(number_of_points_in_mesh,1)
print(action.shape)
# print(z)

ax.plot_surface(x1, y1, action)
ax.set(xlabel='tower available capacity%', ylabel='request power allocation%', zlabel='z', title='z = argmax(qvalue)')
plt.savefig("plot(CC,PA).svg", format="svg")
plt.show()