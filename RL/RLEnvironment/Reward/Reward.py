from abc import abstractmethod


class Reward:

    _reward_value: int

    def __call__(self):
        pass

    @property
    def reward_value(self):
        return self._reward_value

    @reward_value.setter
    def reward_value(self,reward_value):
        self._reward_value = reward_value

