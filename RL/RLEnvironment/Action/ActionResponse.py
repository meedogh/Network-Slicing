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


    def explore(self):
        ac = np.random.choice([0,1])
        return ac

    def exploit(self, model, state):
        # print(" mask exploit : ", mask)
        state = np.array(state).reshape([1, np.array(state).shape[0]])
        c=np.array(model.predict(state, verbose=0))
        c = np.array(c).reshape(1,2)
        return np.argmax(c[0])

    def execute(self, state, action):
        return state.calculate_state()
