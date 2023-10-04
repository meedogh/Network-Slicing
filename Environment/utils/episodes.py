import json

from Environment import env_variables


class Episodes():

    def __init__(self, episode: str):
        self.episode = episode
        self.json_loader()

    def episode_selector(self, mean, std, number, ent_ratio, auto_ratio, safety_ratio,cc,bl):
        env_variables.number_cars_mean_std['mean'] = mean
        env_variables.number_cars_mean_std['std'] = std
        env_variables.threashold_number_veh = number
        env_variables.ENTERTAINMENT_RATIO = ent_ratio
        env_variables.AUTONOMOUS_RATIO = auto_ratio
        env_variables.SAFETY_RATIO = safety_ratio
        env_variables.capacity_mean_std['mean'] = cc
        env_variables.buffer_length_mean_std['mean'] = bl


    def json_loader(self):
        with open("Environment/utils/episodes.json", "r") as json_file:
            data = json.load(json_file)
        self.episode_selector(*data[self.episode])
