from RL.AgentBuilder import ActionBuilder, AgentBuilder_
from RL.DecentralizeModelBuilder import ModelBuilder_Decentralize
from RL.EnvBuilder import EnvironmentBuilder
from RL.CentralizeModelBuilder import ModelBuilder_Centralize
from RL.RLAlgorithms.Centralized_DQN import CentralizeDQN
from keras.optimizers import Adam


class RLBuilder:
    def __init__(self, rl=None):
        if rl is None:
            self.rl = CentralizeDQN()
        else:
            self.rl = rl

    @property
    def model_(self):

        return ModelBuilder(self.rl)

    @property
    def environment(self):
        return EnvBuilder(self.rl)

    @property
    def agent(self):
        return AgentBuilder(self.rl)

    def build(self):
        return self.rl


class EnvBuilder(RLBuilder):
    def __init__(self, rl):
        super().__init__(rl)

    def build_env(self, reward_type, state_type):
        self.rl.environment = (
            EnvironmentBuilder()
            .state()
            .build_state(state_type)
            .reward()
            .build_reward(reward_type)
            .build()
        )
        return self


class AgentBuilder(RLBuilder):
    def __init__(self, rl):
        super().__init__(rl)

    def build_agent(self, action_type):
        self.rl.agents = AgentBuilder_().action().build_action(action_type).build()
        return self


class ModelBuilder(RLBuilder):
    def __init__(self, rl):
        super().__init__(rl)

    def build_model(self, model_type, state_input_size, action_output_size):
        if model_type == "centralized":
            self.rl.model = (
                ModelBuilder_Centralize()
                .state_size()
                .build_state_size(state_input_size)
                .action_size()
                .build_action_size(action_output_size)
                .loss_func()
                .build_loss_func("mse")
                .optimizer()
                .build_optimizer(Adam)
                .activation_func()
                .build_Activation("relu")
                .activation_func_output_layer()
                .build_activation_output("sigmoid")
                .learning_rate()
                .build_Learning_rate(0.5)
                .builder()
            )
        elif model_type == "decentralized":
            self.rl.model = (
                ModelBuilder_Decentralize()
                .state_size()
                .build_state_size(state_input_size)
                .action_size()
                .build_action_size(action_output_size)
                .loss_func()
                .build_loss_func("mse")
                .optimizer()
                .build_optimizer(Adam)
                .activation_func()
                .build_Activation("relu")
                .activation_func_output_layer()
                .build_activation_output("sigmoid")
                .learning_rate()
                .build_Learning_rate(0.5)
                .builder()
            )

        return self

# build = RLBuilder()
# builder = build.agent.build_agent().environment.build_env().model_.build_model().build()

# print(builder.agents)
# print(builder.environment)

# print(builder)

# def fill_grids(outlets):
#     Grids = {
#         "grid1": [],
#         "grid2": [],
#         "grid3": [],
#         "grid4": [],
#     }
#     num_grids = len(Grids)
#     list(map(lambda x: Grids["grid" + str(random.randint(1, num_grids))].append(x), outlets))
#     return Grids
#
# outlet = ThreeG(outlet_types.get("3G"), 0, 1, [1, 1, 1], 1, 1, [10, 15, 22], [10, 20, 30])
# outlet2 = ThreeG(outlet_types.get("3G"), 0, 1, [1, 1, 1], 1, 1, [10, 5, 12], [10, 10, 40])
# outlet3 = ThreeG(outlet_types.get("3G"), 0, 1, [1, 1, 1], 1, 1, [10, 5, 12], [10, 10, 40])
# outlet4 = ThreeG(outlet_types.get("3G"), 0, 1, [1, 1, 1], 1, 1, [10, 5, 12], [10, 10, 40])
# outlet5 = ThreeG(outlet_types.get("3G"), 0, 1, [1, 1, 1], 1, 1, [10, 5, 12], [10, 10, 40])
# outlet6 = ThreeG(outlet_types.get("3G"), 0, 1, [1, 1, 1], 1, 1, [10, 5, 12], [10, 10, 40])
# outlets=[]
# outlets.extend([outlet,outlet2,outlet3,outlet4,outlet5,outlet6])
# Grids = fill_grids(outlets)
#
# build = RLBuilder()
# builder = build.agent.build_agent().environment.build_env().model_.build_model().build()
# builder.agents.grid_outlets = Grids.get("grid1")
# print("... ",builder.agents.grid_outlets)
#
#
# builder.environment.state.allocated_power = outlet.power_distinct
# builder.environment.state.supported_services = outlet.supported_services_distinct
# builder.environment.state.allocated_power = outlet2.power_distinct
# builder.environment.state.supported_services = outlet2.supported_services_distinct
# builder.environment.state.filtered_powers = builder.environment.state.allocated_power
# print("binary .. ", builder.environment.state.supported_services)
# state_value = builder.environment.state.calculate_state(builder.environment.state.supported_services)
#
# print("state_value  ", state_value)
# action, action_value = builder.agents.chain(builder.model, state_value, 0.9)
# print(action)
# print(action_value)
# print(action.execute(builder.environment.state, action_value))
