reward_info_path  = "C:/Users/Windows dunya/PycharmProjects/pythonProject/Network-Slicing/action_each_single_request_reward_method4_add_init_10_11_12_retrain_test/reward_info/reward_info.pkl"
users_logging_info_path = "C:/Users/Windows dunya/PycharmProjects/pythonProject/Network-Slicing/action_each_single_request_reward_method4_add_init_10_11_12_retrain_test/users_logging_info/users_logging_info.pkl"
users_logging_info = []
reward_info=[]
import pickle
with open(reward_info_path, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            reward_info.append(loaded_value)
    except EOFError:
        pass

with open(users_logging_info_path, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            users_logging_info.append(loaded_value)
    except EOFError:
        pass

print(" reward_info : ", reward_info)
print("users_logging_info : ", users_logging_info)