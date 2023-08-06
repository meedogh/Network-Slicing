from itertools import product
import numpy as np


permutations = list(product([0, 1], repeat=3))
action_space = 8
action_permutations_dectionary = {permutations[i]: i for i in range(action_space)}


def available_actions( supported_service):
    indexs_of_not_supported = [index for index, value in enumerate(supported_service) if value == 0]
    not_available_actions = []
    for i in permutations:
        for j in indexs_of_not_supported:
            if i[j] == 1:
                not_available_actions.append(i)

    not_available_actions = set(not_available_actions)
    not_available_actions = list(not_available_actions)
    available_actions = [item for item in permutations if item not in not_available_actions]
    available_mapped_actions = [value for key, value in action_permutations_dectionary.items() if
                                key in available_actions]

    return available_mapped_actions


def action_masking( supported_service):
    available_mapped_actions = available_actions(supported_service)
    action_mask = np.zeros(8)
    for i, value in enumerate(action_mask):
        for j, val in enumerate(available_mapped_actions):
            if action_mask[val] == 0:
                action_mask[val] = 1
    action_mask = np.array(action_mask).reshape([1, np.array(action_mask).shape[0]])
    return action_mask