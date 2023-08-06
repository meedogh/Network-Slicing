from abc import ABC, abstractmethod
from typing import Optional

from RL.RLEnvironment.Action.Action import Action


class IHandler(ABC):
    def __init__(self, action: Action, successor: Optional["IHandler"] = None):
        self.successor = successor
        self.action = action
        self.flag = 0

    def handle(self, test, epsilon):
        self.action = self.check_epsilon(test, epsilon)
        if not hasattr(self.action, 'all'):
            self.action, self.flag = self.successor.handle(test, epsilon)
        return self.action, self.flag

    @abstractmethod
    def check_epsilon(self, test, epsilon) -> Optional[bool]:
        pass


class Explore(IHandler):
    "A Concrete Handler"
    def __init__(self, action, mask, successor):
        super().__init__(action, successor)
        self.mask = mask


    def check_epsilon(self, test, epsilon):
        if 1 > epsilon >= test > 0:
            self.flag = 0
            # action = Action.explore()
            # print(f'handled in {self.__class__.__name__} because epsilon is {epsilon} and random is {test}')
            explore_val = self.action.explore(self.mask)
            return explore_val


class Exploit(IHandler):
    "A Concrete Handler"
    def __init__(self, action, model, state,mask, successor):
        super().__init__(action, successor)
        self.model = model
        self.state = state
        self.mask = mask
    def check_epsilon(self, test, epsilon):
        if 0 < epsilon < test < 1:
            self.flag = 1
            # action = Action.exploit()
            # print(f'handled in {self.__class__.__name__} because epsilon is {epsilon} and random is {test}')
            exploit = self.action.exploit(self.model, self.state,self.mask)
            return exploit


class FallbackHandler(IHandler):
    def check_epsilon(self, test, epsilon):
        # print(f'handled in {self.__class__.__name__}')
        raise ValueError("epsilon must be in range 0 to 1 :", epsilon)
