from abc import ABCMeta


class RLMeta(type):
    def __new__(mcs, name, bases, class_dict):
        class_ = super().__new__(mcs, name, bases, class_dict)
        # call the parent class's __new__ method to create the class

        # make sure the new class has agent and env attributes
        if not hasattr(class_, 'agents') or not hasattr(class_, 'environment'):
            raise NotImplementedError("Classes with RLMeta as metaclass must have 'agents' and 'env' attributes")

        return class_

    def get_agent_observation(cls):
        if cls.agent is None:
            raise ValueError("Agent is not initialized")
        print('n',cls.agent)

    def get_env_observation(cls):
        if cls.environment is None:
            raise ValueError("Env is not initialized")
        return cls.environment.observe()


def rlabc(cls):
    return ABCMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))
