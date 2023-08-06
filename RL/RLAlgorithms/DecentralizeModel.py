from keras import Sequential
from keras.layers import Dense, Reshape
import  tensorflow as tf
from keras.optimizers import Adam
from keras.models import load_model
from itertools import product
from keras.layers import Input, Dense, Lambda
from keras.models import Model
class DecentralizeModel():
    def __init__(self, state_size = 5, action_size =8, activation_function = "relu", loss_function = "mse", optimization_algorithm = Adam,
                 learning_rate = 0.5, output_activation = "tanh", **kwargs):
        self.state_size = state_size
        self.action_size = action_size
        self.activation_function = activation_function
        self.loss_function = loss_function
        self.optimization_algorithm = optimization_algorithm
        self.learning_rate = learning_rate
        self.output_activation = output_activation


    # def build_model(self) -> Sequential:
    #     model_ = Sequential()
    #     model_.add(Dense(24, input_dim=self.state_size, activation=self.activation_function))
    #     model_.add(Dense(24, activation=self.activation_function))
    #     model_.add(Dense(2 , activation=self.output_activation))
    #     # model_.add(Reshape((2,1)))
    #     model_.compile(loss=self.loss_function,
    #                    optimizer=self.optimization_algorithm(learning_rate=self.learning_rate))
    #     return model_
    def build_model(self) -> Model:
        state_input = Input(shape=(self.state_size,))
        action_mask_input = Input(shape=(self.action_size,))

        x = Dense(64, activation=self.activation_function , name= "dens1")(state_input)
        x = Dense(64, activation=self.activation_function , name= "dens2")(x)

        logits = Dense(self.action_size,activation=self.output_activation,name= "logits")(x)

        masked_logits = Lambda(lambda x: x[0] + (1 - x[1]) * -1e25)([logits, action_mask_input])
        action_probs = tf.nn.softmax(masked_logits)
        model = Model(inputs=[state_input, action_mask_input], outputs=action_probs)
        model.compile(loss=self.loss_function,
                      optimizer=self.optimization_algorithm(learning_rate=self.learning_rate))
        return model
    def save(self, filename):
        self.save_model(filename)

    def load(self, filename):
        return load_model(filename)

    def load_weights(self, filename):
        """ Load model from file. """
        self.load_weights(filename)

    def save_weights(self, filename):
        """ Save model to file. """
        self.save_weights(filename)

    def predict(self, state):
        """ Predict value based on state. """
        pass
