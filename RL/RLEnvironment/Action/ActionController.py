from RL.RLEnvironment.Action.Action import Action
from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment


class ActionController:
    _command: ActionAssignment

    # print("comm ",self._command)

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, comm):
        self._command = comm

    def execute(self, state, action_decision):
        next_state = self.command.execute(state, action_decision)
        return next_state

    def explore(self):
        return self.command.explore()


    def exploit(self, model, state):
        """
        this function for expoilfvdbvjfbvndkfbkjdfjbmdbvkjdfkdfkdfkmdfkmfdkmdfkmdfkgvkldkldfk
        """
        return self.command.exploit(model, state )





