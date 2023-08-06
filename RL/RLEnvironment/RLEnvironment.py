from typing import Protocol, runtime_checkable

from RL.RLEnvironment.Reward.Reward import Reward
from RL.RLEnvironment.State.State import State

@runtime_checkable
class RLProtocol(Protocol):
    state: State
    reward: Reward


class RLEnvironment():
    def __init__(self):
        self._state = None
        self._reward = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, s):
        self._state = s

    @property
    def reward(self):
        return self._reward

    @reward.setter
    def reward(self, r):
        self._reward = r


# yara = RLEnvironment(State(), Reward(9))

# print(isinstance(yara,RLProtocol))