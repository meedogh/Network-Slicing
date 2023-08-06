import random

import numpy as np
from RL.RLEnvironment.Action.Action import Action


class ActionResponse:
    def __init__(self):
        self.grid_cell = 3
        self.num_services = 3
        self._action_value_decentralize = 0
        self._action_flags = []
        self._action_object = None

    @property
    def action_object(self):
        return self._action_object

    @action_object.setter
    def action_object(self, value):
        self._action_object = value
    @property
    def action_flags(self):
        return self._action_flags

    @action_flags.setter
    def action_flags(self, value):
        self._action_flags = value
    @property
    def action_value_decentralize(self):
        return self._action_value_decentralize
    @action_value_decentralize.setter
    def action_value_decentralize(self,val):
        self._action_value_decentralize = val


    def explore(self,action_mask):
        available_actions=[]
        action_mask = action_mask[0]
        # print("mask in explor :",action_mask)
        for i in range(len(action_mask)):
            if action_mask[i] == 1 :
                available_actions.append(i)
        # print("available_actions : ",available_actions)
        ac = np.random.choice(available_actions)
        return ac

    def exploit(self, model, state,mask):
        # print(" mask exploit : ", mask)
        state = np.array(state).reshape([1, np.array(state).shape[0]])
        c=np.array(model.predict([state,mask], verbose=0))
        c = np.array(c).reshape(1,8)
        return np.argmax(c[0])

    def execute(self, state, action):
        return state.calculate_state()
