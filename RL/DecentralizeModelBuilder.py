from keras.optimizers import Adam

from RL.RLAlgorithms.DecentralizeModel import DecentralizeModel


class ModelBuilder_Decentralize:

    def __init__(self, model=None):
        if model is None:
            self.model = DecentralizeModel(state_size=7, action_size=8,
                               activation_function="relu", loss_function="mse", optimization_algorithm=Adam,
                               learning_rate=0.5, output_activation="sigmoid").build_model()
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


class StateSizeBuilder(ModelBuilder_Decentralize):
    def __init__(self, model):
        super().__init__(model)

    def build_state_size(self, size):
        self.model.state_size = size
        return self


class ActionSizeBuilder(ModelBuilder_Decentralize):
    def __init__(self, model):
        super().__init__(model)

    def build_action_size(self, size):
        self.model.action_size = size
        return self


class LossFuncBuilder(ModelBuilder_Decentralize):
    def __init__(self, model):
        super().__init__(model)

    def build_loss_func(self, loss):
        self.model.loss_function = loss
        return self


class OptimizerBuilder(ModelBuilder_Decentralize):
    def __init__(self, model):
        super().__init__(model)

    def build_optimizer(self, optimizer):
        self.model.optimization_algorithm = optimizer
        return self


class ActivationFuncOutputBuilder(ModelBuilder_Decentralize):
    def __init__(self, model):
        super().__init__(model)

    def build_activation_output(self, activation):
        self.model.output_activation = activation
        return self


class ActivationFuncBuilder(ModelBuilder_Decentralize):
    def __init__(self, model):
        super().__init__(model)

    def build_Activation(self, activation):
        self.model.activation_function = activation
        return self


class LearningRateBuilder(ModelBuilder_Decentralize):
    def __init__(self, model):
        super().__init__(model)

    def build_Learning_rate(self, learning):
        self.model.learning_rate = learning
        return self