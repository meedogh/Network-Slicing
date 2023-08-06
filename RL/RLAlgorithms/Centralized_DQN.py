from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from RL.RLAlgorithms.AbstractRL import AbstractRL


# from RL.RLAlgorithms.Model import Model
# from RL.Agent.Agent import Agent
# from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment
# from RL.RLEnvironment.RLEnvironment import RLEnvironment
# from Communications.BridgeCommunications.ComsThreeG import ComsThreeG
# from Outlet.Cellular.ThreeG import ThreeG
# from RL.RLEnvironment.State.CentralizedState import CentralizedState
# from RL.RLEnvironment.State.DecentralizedState import DeCentralizedState
#

class CentralizeDQN(AbstractRL):
    def init(self, *args):
        super().init(*args)

    # def create_model(self) -> Sequential:
    #    return self.model.build_model()

    def __str__(self):
        return f"evironment :  {self._environment} , agents : {self._agents} , model : {self._model}"

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, m):
        self._model = m



    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, e):
        self._environment = e

    @property
    def agents(self):
        return self._agents

    @agents.setter
    def agents(self, a):
        self._agents = a

    def create_model(self):
        print("1")

