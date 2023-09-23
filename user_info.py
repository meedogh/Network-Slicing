
import pickle

# Assuming you have a pickle file named 'data.pkl'
pickle_file_path = 'C:/Users/Windows dunya/PycharmProjects/pythonProject/Network-Slicing/action_each_single_request_reward_method4_add_init_10_11_12/users_logging_info/users_logging_info.pkl'
abort_req = []
# Open the pickle file in read mode
with open(pickle_file_path, "rb") as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            abort_req.append(loaded_value)
    except EOFError:
        pass

print(abort_req)
# for key , values in data.items():
#     print(key)
# 'data' now contains the contents of the pickle file
