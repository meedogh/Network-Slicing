from abc import abstractmethod
from collections import deque
from typing import runtime_checkable, Protocol
from RL.RLEnvironment.Action.ActionController import ActionController


@runtime_checkable
class AgentProtocol(Protocol):
    action: ActionController

    def q(self):
        pass


class AbstractAgent():
    #epsilon=0.95, gamma=0.95, epsilon_decay=0.000025, min_epsilon=0.70,
    def __init__(self, epsilon=0.95, gamma=0.95, epsilon_decay=0.000075, min_epsilon=0.01,
                 episodes=7,
                 cumulative_reward=0,
                 step=60):
        self._action = None
        # self.action_type = ActionController()
        self.epsilon = epsilon
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.episodes = episodes
        self.cumulative_reward = cumulative_reward
        self.step = step
        self.memory = deque(maxlen=750)
        self.batch_size = 32
        self.epsilon_max = 0.95
        # model state action reward

    @property
    @abstractmethod
    def action(self):
        pass

    @action.setter
    @abstractmethod
    def action(self, a):
        pass

    @abstractmethod
    def replay_buffer_centralize(self, batch_size, model):
        pass

    @abstractmethod
    def replay_buffer_decentralize(self, batch_size, model):
        pass

    @abstractmethod
    def remember(self,flag, state, action, reward, next_state):
        pass



    @abstractmethod
    def train(self, builder, **kwargs):
        """ Train model. """
        pass

    def q(self, state):
        """ Return q values for state. """
        pass

    @abstractmethod
    def chain(self, model, state, epsilon):
        pass


