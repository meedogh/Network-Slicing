from RL.RLEnvironment.RLEnvironment import RLEnvironment



class EnvironmentBuilder:
    def __init__(self, env=None):
        if env is None:
            self.env = RLEnvironment()
        else:
            self.env = env

    def __str__(self):
        return f" state : {self.env.state} , env : {self.env.reward}"

    def state(self):
        return StateBuilder(self.env)

    def reward(self):
        return RewardBuilder(self.env)

    def build(self):
        return self.env


class StateBuilder(EnvironmentBuilder):
    def __init__(self, env):
        super().__init__(env)

    def build_state(self,state_type):
        self.env.state = state_type
        #CentralizedState()
        return self




class RewardBuilder(EnvironmentBuilder):
    def __init__(self, env):
        super().__init__(env)

    def build_reward(self,reward_type):
        self.env.reward = reward_type
        #CentralizedReward()
        # cr.services_requested = np.array([30, 40, 10])
        # cr.services_ensured = np.array([5, 10, 3])
        # cr.services_ensured = np.array([3, 2, 1])
        # reward = cr.calculate_reward()
        # self.env.reward = reward
        # print("reward is : ", reward)
        return self

# en = EnvironmentBuilder()
# en = en \
#     .state() \
#     .build_state("1") \
#     .reward() \
#     .build_reward("2") \
#
# print(en)
# print(en.build())
