import os

import keras

import random
from RL.Agent.IAgent import AbstractAgent
from RL.RLEnvironment.Action.ActionChain import Exploit, Explore, FallbackHandler
import pickle
import tensorflow as tf
import numpy as np
from Environment.utils.mask_generation import *

class Agent(AbstractAgent):
    _grid_outlets = []
    _action_value = 0
    _outlets_id = []

    def __init__(self, *args):
        super().__init__(*args)
        self._outlets_id = []
        self._grid_outlets = []
        self._action_value = 0
        self._qvalue = 0.0
        self.mask = []

    @property
    def outlets_id(self):
        return self._outlets_id

    @outlets_id.setter
    def outlets_id(self, id_):
        self._outlets_id = id_

    @property
    def qvalue(self):
        return self._qvalue

    @qvalue.setter
    def qvalue(self, q):
        self._qvalue = q

    @property
    def grid_outlets(self):
        return self._grid_outlets

    @grid_outlets.setter
    def grid_outlets(self, list_):
        # print("here : ", list_)
        self._grid_outlets = list_

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, a):
        self._action = a

    @property
    def action_value(self):
        return self._action_value

    @action_value.setter
    def action_value(self, a):
        self._action_value = a



    def replay_buffer_decentralize(self, batch_size, model):
        minibatch = random.sample(self.memory, batch_size)
        target = 0
        for exploitation, state, action, reward, next_state in minibatch:
            # print("inside replay buffer ")
            target = reward
            if next_state is not None:
                next_state = np.array(next_state).reshape([1, np.array(next_state).shape[0]])
                # logit_model2 = keras.Model(inputs=model.input, outputs=model.layers[-2].output)
                logit_value = model.predict(next_state, verbose=0)[0]
                target = reward + self.gamma * np.amax(logit_value)
            # print("target belman :   ",target)
            state = np.array(state).reshape([1, np.array(state).shape[0]])
            target_f = model.predict(state, verbose=0)
            # print("target model : ", target_f)
            target_f[0][action] = target
            # print("target f after assign belman : ", target_f)
            model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.min_epsilon:
            self.epsilon -= self.epsilon * self.epsilon_decay
        return target

    def replay_buffer_centralize(self, batch_size, model):
        minibatch = random.sample(self.memory, batch_size)
        target = []
        for exploitation, state, action, reward, next_state in minibatch:
            target = reward
            if next_state is not None:
                next_state = np.array(next_state).reshape([1, np.array(next_state).shape[0]])
                model_qvalue = model.predict(next_state, verbose=0)[0]

                if exploitation == 0:
                    # print("exploration : centralize ")
                    target = reward + self.gamma * model_qvalue[action]
                elif exploitation == 1:
                    # print("exploitaion : centralize ")
                    target = reward + self.gamma * np.amax(model_qvalue)

            state = np.array(state).reshape([1, np.array(state).shape[0]])
            target_f = np.round(model.predict(state, verbose=0))
            ########################################### note for rounding
            target_f[0][action] = target
            model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.min_epsilon:
            self.epsilon -= self.epsilon * self.epsilon_decay
        return target

    def free_up_memory(self, deque, filename):
        mode = 'wb' if not os.path.exists(filename) else 'ab'
        with open(filename, mode) as file:
            for item in deque:
                pickle.dump(item, file)
        deque.clear()

    def fill_memory(self, deque, filename):
        with open(filename, 'rb') as file:
            try:
                while True:
                    loaded_value = pickle.load(file)
                    deque.append(loaded_value)
            except EOFError:
                pass

    def remember(self, flag, state, action, reward, next_state):
        self.memory.append((flag, state, action, reward, next_state))

    def remember_decentralize(self, flag, state, action, reward, next_state, rem):
        if rem:
            # print(supported_services, "  \n  ",flag  , "  \n  ", state, "  \n  ", action, "  \n  ", reward, "  \n  ", next_state)
            self.memory.append(( flag, state, action, reward, next_state))

    def chain_dec(self, model, state, epsilon):
        "A chain with a default first successor"
        test = np.random.rand()
        "Setting the first successor that will modify the payload"
        action = self.action
        handler = Exploit(action, model, state,
                          Explore(action, FallbackHandler(action)))
        action_Value, flag = handler.handle(test, epsilon)
        # print("action value inside chain : ",action_Value )
        return action, action_Value, flag

    def chain(self, model, state, epsilon):
        "A chain with a default first successor"
        test = np.random.rand()
        "Setting the first successor that will modify the payload"
        action = self.action
        handler = Exploit(action, model, state, Explore(action, FallbackHandler(action)))
        action_Value, flag = handler.handle(test, epsilon)
        return action, np.where(action_Value > 0.5, 1, 0), flag

    def exploitation(self, model, state):
        action = self.action
        action_value = self.action.exploit(model, state)
        flag = 1
        return action, np.where(action_value > 0.5, 1, 0), flag

    def heuristic_action(self, gridcell, current_services_power_allocation, current_services_requested,
                         number_of_periods_until_now):
        outlets = []
        flags = np.zeros(9)
        # flags = 0
        for j, outlet in enumerate(gridcell.agents.grid_outlets):
            outlets.append(outlet)
        list_power = [0, 0, 0]
        list_requested = [0, 0, 0]
        dic_power_with_index = {}
        dec_requested_with_index = {}
        for out in outlets:
            for i in range(3):
                list_power[i] = list_power[i] + current_services_power_allocation[out][i]
                list_requested[i] = list_requested[i] + current_services_requested[out][i]
        for i in range(3):
            dic_power_with_index[i] = list_power[i]
            dec_requested_with_index[i] = list_requested[i]
        the_sorted_current_power = dict(sorted(dic_power_with_index.items(), key=lambda x: x[1]))
        the_sorted_current_power_copy = dict(sorted(dic_power_with_index.items(), key=lambda x: x[1]))

        outlets.reverse()
        for j, out in enumerate(outlets):
            out.supported_services = [0, 0, 0]
            count_zero = 0
            copy_current = out.current_capacity
            for i in range(3):
                key = list(the_sorted_current_power_copy.keys())[i]
                power = the_sorted_current_power_copy[key]
                requested = dec_requested_with_index[key]
                average = 0

                if number_of_periods_until_now > 0:
                    average = power / number_of_periods_until_now

                if copy_current >= average and average > 0.0:
                    out.supported_services[key] = 1
                    copy_current = out.current_capacity - average
                    the_sorted_current_power_copy[key] = 0
                elif average == 0.0:
                    out.supported_services[key] = 0
                elif copy_current == 0:
                    out.supported_services[key] = 0
                elif copy_current < average:
                    if copy_current >= average * 0.4:
                        out.supported_services[key] = 1
                        the_sorted_current_power_copy[key] = abs(the_sorted_current_power_copy[key] - copy_current)
                        copy_current = 0
                        break
            # print(f"out {out.supported_services}")
        return flags
