import json

from Environment import env_variables


class Period:
    def __init__(self, period: str):
        self.period = period
        self.json_loader()

    def period_selector(self, mean, std, number, ent_ratio, auto_ratio, safety_ratio):
        env_variables.number_cars_mean_std['mean'] = mean
        env_variables.number_cars_mean_std['std'] = std
        env_variables.threashold_number_veh = number
        env_variables.ENTERTAINMENT_RATIO = ent_ratio
        env_variables.AUTONOMOUS_RATIO = auto_ratio
        env_variables.SAFETY_RATIO = safety_ratio

    # day time
    def json_loader(self):
        with open("Environment/utils/period.json", "r") as json_file:
            data = json.load(json_file)
        self.period_selector(*data[self.period])

