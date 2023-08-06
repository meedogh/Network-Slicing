from abc import ABC, abstractmethod


class State(ABC):
    def __call__(self, *args, **kwargs):
        pass

    def __init__(self):
        pass

    @abstractmethod
    def calculate_state(self, **kwargs):
        pass
