from RL.ActionBuilder import ActionBuilder_
from RL.Agent.Agent import Agent


class AgentBuilder_:
    def __init__(self, agent=None):
        if agent is None:
            self.agent = Agent()
        else:
            self.agent = agent

    def __str__(self):
        return f"action : {self.agent.action}"

    def action(self):
        return ActionBuilder(self.agent)


    def build(self):
        return self.agent


class ActionBuilder(AgentBuilder_):
    def __init__(self, agent):
        super().__init__(agent)

    def build_action(self,action_type):
        self.agent.action = ActionBuilder_().command().build_command(action_type).build()
        return self



# act = AgentBuilder_()
# act = act \
#     .action() \
#     .build_action()\
#     .grid_outlet()\
#     .build_grid_outlets("grid1")
#
# print(act)
# print(act.build())

