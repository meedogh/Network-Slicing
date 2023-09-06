import numpy as np
import matplotlib.pyplot as plt
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from mpl_toolkits.mplot3d import Axes3D
import pickle as pk

file_serve = "C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//served_state.pkl"
serve = []
with open(file_serve, 'rb') as file:
    try:
        while True:
            loaded_value = pk.load(file)
            serve.append(loaded_value)
    except EOFError:
        pass

x1 = []
x2 = []
states =[]
for i in serve:
    x1.append(i[0])
    x2.append(i[2])
    states.append(i)

x1= x1[-10:]
x2= x2[-10:]
states = states[-10:]
# Create a grid of (x1, x2) pairs
X1, X2 = np.meshgrid(x1, x2)


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
Q_values = []
for i in range(10):
    states[i] = np.array(states[i]).reshape([1, np.array(states[i]).shape[0]])
    Q_values.append(np.argmax(model.predict(states[i])))
print(len(Q_values))
print(np.array(Q_values).shape)
print(np.array(X1).shape)
print(np.array(X2).shape)

# Flatten X1 and X2
# Flatten X1 and X2
X1_flat = X1.flatten()
X2_flat = X2.flatten()

# Create a 3D scatter plot for the Q-values
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(X1_flat, X2_flat, Q_values, c=Q_values, cmap='viridis', marker='o', label='Q-values')

# Set axis labels
ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.set_zlabel('Q-value')

# Add a colorbar
cbar = fig.colorbar(scatter)
cbar.set_label('Q-value')

# Show the plot
plt.show()


