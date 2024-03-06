import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

def load_data(folder, filename_pattern):
    data = []
    for file in os.listdir(folder):
        if file.startswith(filename_pattern) and file.endswith(".pkl"):
            file_path = os.path.join(folder, file)
            with open(file_path, "rb") as f:
                while True:
                    try:
                        data.append(pickle.load(f))
                    except EOFError:
                        break
    return data

def save_served_requests(folder_path, j, served_requests):
    served_requests_folder = os.path.join(folder_path, "serving_ratio")
    os.makedirs(served_requests_folder, exist_ok=True)
    file_path = os.path.join(served_requests_folder, f"serving_ratio{j}.pkl")
    
    # Cut off data after the first occurrence of 0
    zero_index = np.where(served_requests <= 0.1019)[0][0]
    print(zero_index)
    # if len(zero_index) > 0:
    print(served_requests)
    served_requests = served_requests[:zero_index]
    with open(file_path, "wb") as f:
        pickle.dump(served_requests, f)

def save_folders(folder_paths, title):
    for folder_path in folder_paths:
        for j in range(0, 1):
            all_generated = []
            all_served = []
            all_ratio = []

            folder_generated = os.path.join(folder_path, f"generated_requests_over_simulation")
            all_generated.extend(load_data(folder_generated, f"generated_requests_over_simulation{j}"))
            
            folder_served = os.path.join(folder_path, f"served_requests_over_simulation")
            all_served.extend(load_data(folder_served, f"served_requests_{j}"))
            
            folder_ratio = os.path.join(folder_path, f"serving_ratio")
            all_ratio.extend(load_data(folder_ratio, f"serving_ratio{j}"))

            min_length = min(len(all_generated), len(all_served))

            all_generated = np.array(all_generated[1:min_length])
            all_served = np.array(all_served[1:min_length])

            serving_ratio = all_served / all_generated
            serving_ratio = all_ratio[0]

            # print(min(serving_ratio))
            print(serving_ratio)
            plt.plot(serving_ratio)
            plt.show()
            # save_served_requests(folder_path, j, serving_ratio)

def main():
    fifo_folder_paths = ["run_rl_scenario_2_lr_0.001"]
    save_folders(fifo_folder_paths, "FIFO")

if __name__ == "__main__":
    main()
