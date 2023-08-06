from abc import abstractmethod

from RL.RLMeta import RLMeta, rlabc


@rlabc
class AbstractRL(metaclass=RLMeta):
    _agents = []
    _environment = None
    _model = None

    def __init__(self):
        self._agents = None
        self._environment = None
        self._model = None

    def len_(self):
        return len(self._agents)

    @property
    @abstractmethod
    def environment(self):
        # return self._env
        pass

    @environment.setter
    @abstractmethod
    def environment(self, env):
        # self._env = env
        pass

    @property
    @abstractmethod
    def agents(self):
        # return self.agents
        pass

    @property
    @abstractmethod
    def model(self):
        # return self.agents
        pass

    @model.setter
    @abstractmethod
    def model(self, m):
        # self.agents.append(agent)
        pass
    @agents.setter
    @abstractmethod
    def agents(self, agent):
        # self.agents.append(agent)
        pass

    @abstractmethod
    def create_model(self):
        pass
