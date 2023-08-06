from RL.RLEnvironment.Action.ActionController import ActionController
from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment


class ActionBuilder_:
    def __init__(self, action=None):
        if action is None:
            self.action = ActionController()
        else:
            self.action = ActionController()

    def build(self):
        return self.action

    def command(self):
        return CommandBuilder(self.action)

    def __str__(self):
        return f"command is : {self.action.command}"


class CommandBuilder(ActionBuilder_):
    def __init__(self, action):
        super().__init__(action)

    def build_command(self,action_type):
        self.action.command = action_type
        #ActionAssignment()
        return self


# action_comm = ActionController()
# ab = ActionBuilder_()
# ab = ab \
#     .command() \
#     .build_command()
# print(ab)
# print(ab.build())


