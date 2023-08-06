from keras.optimizers import Adam

from RL.RLAlgorithms.CentralizeModel import CentralizeModel


class ModelBuilder_Centralize:

    def __init__(self, model=None):
        if model is None:
            self.model = CentralizeModel(state_size=12, action_size=2,
                               activation_function="relu", loss_function="mse", optimization_algorithm=Adam,
                               learning_rate=0.5, output_activation="sigmoid").build_model()
                # .load_weights("sH://work_projects//network_slicing//ns//results//results//centralized_weight//weights_0.hdf5")
        else:
            self.model = model

    def builder(self):
        return self.model

    def state_size(self):
        return StateSizeBuilder(self.model)

    def action_size(self):
        return ActionSizeBuilder(self.model)

    def loss_func(self):
        return LossFuncBuilder(self.model)

    def optimizer(self):
        return OptimizerBuilder(self.model)

    def activation_func_output_layer(self):
        return ActivationFuncOutputBuilder(self.model)

    def activation_func(self):
        return ActivationFuncBuilder(self.model)

    def learning_rate(self):
        return LearningRateBuilder(self.model)


class StateSizeBuilder(ModelBuilder_Centralize):
    def __init__(self, model):
        super().__init__(model)

    def build_state_size(self, size):
        self.model.state_size = size
        return self


class ActionSizeBuilder(ModelBuilder_Centralize):
    def __init__(self, model):
        super().__init__(model)

    def build_action_size(self, size):
        self.model.action_size = size
        return self


class LossFuncBuilder(ModelBuilder_Centralize):
    def __init__(self, model):
        super().__init__(model)

    def build_loss_func(self, loss):
        self.model.loss_function = loss
        return self


class OptimizerBuilder(ModelBuilder_Centralize):
    def __init__(self, model):
        super().__init__(model)

    def build_optimizer(self, optimizer):
        self.model.optimization_algorithm = optimizer
        return self


class ActivationFuncOutputBuilder(ModelBuilder_Centralize):
    def __init__(self, model):
        super().__init__(model)

    def build_activation_output(self, activation):
        self.model.output_activation = activation
        return self


class ActivationFuncBuilder(ModelBuilder_Centralize):
    def __init__(self, model):
        super().__init__(model)

    def build_Activation(self, activation):
        self.model.activation_function = activation
        return self


class LearningRateBuilder(ModelBuilder_Centralize):
    def __init__(self, model):
        super().__init__(model)

    def build_Learning_rate(self, learning):
        self.model.learning_rate = learning
        return self

# mo = ModelBuilder_Centralize()
# m = mo \
#     .state_size().build_state_size(3) \
#     .action_size().build_action_size(4) \
#     .loss_func().build_loss_func("mse") \
#     .optimizer().build_optimizer(Adam) \
#     .activation_func().build_Activation("relu") \
#     .activation_func_output_layer().build_activation_output("sigmoid") \
#     .learning_rate().build_Learning_rate(0.5)\
#     .builder()
# print(m)
