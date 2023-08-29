import pickle as pk

import numpy as np
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

deque = []

file_name="C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//time_out_next_state.pkl"
with open(file_name, 'rb') as file:
    try:
        while True:
            loaded_value = pk.load(file)
            deque.append(loaded_value)
    except EOFError:
        pass


def build_model() -> Sequential:
        model_ = Sequential()
        model_.add(Dense(24, input_dim=5, activation='relu'))
        model_.add(Dense(24, activation='relu'))
        model_.add(Dense(2, activation='sigmoid'))
        # model_.add(Reshape((3, 3)))
        model_.compile(loss='mse',
                       optimizer=Adam(learning_rate=0.5))
        return model_

model =  build_model()
model.load_weights('C://Users//Windows dunya//PycharmProjects//pythonProject//action_each_single_request_reward2_method2_repeat_periods_each_episode_retrain//decentralized_weights/weights_0_100.hdf5')
for i in deque :
    print("state : ", i)
    state = np.array(i).reshape([1, np.array(i).shape[0]])
    pred = model.predict(state)
    print(pred)
    print(np.argmax(pred[0]))
