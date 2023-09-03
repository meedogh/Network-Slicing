import pickle as pk
import random

import numpy as np
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

wait_to_serve = []
time_out=[]
reject=[]
serve=[]
file_wait_to_serve="C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//test_files//wait_to_serve_state.pkl"
file_time_out="C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//test_files//time_out_state.pkl"

file_reject="C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//test_files//rejected_state.pkl"
file_served="C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//test_files//served_state.pkl"

with open(file_wait_to_serve, 'rb') as file:
    try:
        while True:
            loaded_value = pk.load(file)
            wait_to_serve.append(loaded_value)
    except EOFError:
        pass

with open(file_time_out, 'rb') as file:
    try:
        while True:
            loaded_value = pk.load(file)
            time_out.append(loaded_value)
    except EOFError:
        pass
with open(file_served, 'rb') as file:
    try:
        while True:
            loaded_value = pk.load(file)
            serve.append(loaded_value)
    except EOFError:
        pass
with open(file_reject, 'rb') as file:
    try:
        while True:
            loaded_value = pk.load(file)
            reject.append(loaded_value)
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


print(len(wait_to_serve))
model =  build_model()
model.load_weights('C://Users//Windows dunya//PycharmProjects//pythonProject//Network-Slicing//action_each_single_request_reward2_method2_repeat_periods_each_episode_retrain_buffer_percentage_small_time_out//decentralized_weights/weights_0_140.hdf5')

wait_to_serve.extend(serve)
wait_to_serve.extend(time_out)
wait_to_serve.extend(reject)

shuffled_list = random.sample(wait_to_serve, len(wait_to_serve))
for state in shuffled_list:
    print(" reject state : ", state)
    # print("serve state : ",serve)
    # print("time out state : ",timeout)
    # print("rejected state : ", rej)
    #,serve,time_out,reject
    #serve,timeout,rej
    state = np.array(state).reshape([1, np.array(state).shape[0]])
    pred = model.predict(state)
    print(pred)
    print("output of the model : ",np.argmax(pred[0]))
