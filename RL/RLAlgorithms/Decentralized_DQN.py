
from RL.RLAlgorithms.AbstractRL import AbstractRL


class DecentralizeDQN(AbstractRL):
    def __init__(self, model, *args):
        super().__init__(*args)
        self.model = model



    def load(self, filename):
        self.model.load(filename)

    def save(self, filename):
        self.model.save(filename)

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, e):
        self._env = e

    @property
    def agents(self):
        return self._agents

    @agents.setter
    def agents(self, a):
        self._agents = a



