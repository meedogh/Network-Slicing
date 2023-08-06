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

    def explore(self,mask=None):
        if not hasattr(mask , 'all'):
            if mask!=None :
                if len(mask)>0:
                    # print("mask len : ", len(mask))

                    return self.command.explore(mask)
            else :
                return self.command.explore()
        else :
            return self.command.explore(mask)


    def exploit(self, model, state,mask=None):
        # print("mask : ",mask)
        if not hasattr(mask , 'all'):
            if mask!=None :
                if len(mask)>0:
                    # print("mask len : ", len(mask))

                    return self.command.exploit(model, state ,mask)
            else :
                return self.command.exploit(model, state )
        else :
            return self.command.exploit(model, state, mask)




