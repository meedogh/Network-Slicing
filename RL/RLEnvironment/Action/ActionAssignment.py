import random

import numpy as np
from RL.RLEnvironment.Action.Action import Action


class ActionAssignment:
    def __init__(self):
        self.grid_cell = 3
        self.num_services = 3
        self._action_value_centralize = [0 for _ in range(9)]
        self._action_objects = [0 for _ in range(9)]
        self._action_flags = [0 for _ in range(9)]
        # self._action_value_centralize = 0
        # self._action_objects = None
        # self._action_flags = 0
    @property
    def action_objects(self):
        return self._action_objects
    @action_objects.setter
    def action_objects(self,value):
        self._action_objects = value

    @property
    def action_flags(self):
        return self._action_flags
    @action_flags.setter
    def action_flags(self,value):
        self._action_flags = value
    @property
    def action_value_centralize(self):
        return self._action_value_centralize
    @action_value_centralize.setter
    def action_value_centralize(self,val):
        self._action_value_centralize = val

    def explore(self):
        ac = np.random.choice([0,1])
        return ac

    def exploit(self, model, state ):
        #return np.array(model.predict(state, verbose=0).reshape(3, 3), )
        # print("choose exploit")
        # print("state shape : ", np.array(state).shape)
        state = np.array(state).reshape([1, np.array(state).shape[0]])
        c = np.array(model.predict(state, verbose=0)).reshape(1, 2)
        return np.argmax(c[0])

    def execute(self, state, action_decision):
        # state.supported_services = action_decision
        # print(" state.calculate_state() : " , v )
        return state.calculate_state()
