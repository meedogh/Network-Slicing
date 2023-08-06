from typing import Protocol


class Action(Protocol):
    def execute(self, state, **kwargs):
        ...

    def explore(self,supported):
        ...

    def exploit(self, model, state,mask):
        ...
