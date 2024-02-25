import os
import pickle
import matplotlib.pyplot as plt
import numpy as np


def load_data(folder, filename_pattern):
    data = []
    for file in os.listdir(folder):
        if file.startswith(filename_pattern) and file.endswith(".pkl"):
            file_path = os.path.join(folder, file)
            with open(file_path, "rb") as f:
                while True:
                    try:
                        loaded_data = pickle.load(f)
                        if isinstance(loaded_data, list):
                            data.extend([np.array(d) for d in loaded_data])
                        else:
                            data.append(np.array(loaded_data))
                    except EOFError:
                        break
    return data


def main():
    fifo_folder_paths = [f"run_fifo_scenario_1_lr_0.001"]
    rl_folder_paths = [f"run_rl_scenario_1_lr_0.001"]

    all_served_fifo = np.array([])
    all_served_rl = np.array([])

    all_generated_fifo = np.array([])
    all_generated_rl = np.array([])
    
    for folder_path in fifo_folder_paths:
        served = np.array([])
        generated = np.array([])

        for j in range(0, 1):
            folder_served = os.path.join(folder_path, f"served_requests_over_simulation")
            served_data = np.array(load_data(folder_served, f"served_requests_{j}")) 

            folder_generated = os.path.join(folder_path, f"generated_requests_over_simulation")
            generated_data = np.array(load_data(folder_generated, f"generated_requests_over_simulation{j}")) 
            # plt.plot(served_data/generated_data)
            # plt.show()
            folder_ratio = os.path.join(folder_path, f"serving_ratio")
            served_ratio = np.array(load_data(folder_ratio, f"serving_ratio{j}")) 
            plt.plot(served_ratio[0])
            plt.show()

            served_data_flat = served_data.flatten()
            generated_data_flat = generated_data.flatten()

            served = np.concatenate((served, served_data_flat))
            generated = np.concatenate((generated, generated_data_flat))

        all_served_fifo = np.concatenate((all_served_fifo, served))
        all_generated_fifo = np.concatenate((all_generated_fifo, generated))

    for folder_path in rl_folder_paths:
        served = np.array([])
        generated = np.array([])

        for j in range(0, 1):
            folder_served = os.path.join(folder_path, f"served_requests_over_simulation")
            served_data = np.array(load_data(folder_served, f"served_requests_{j}")) 
            
            folder_ratio = os.path.join(folder_path, f"serving_ratio")
            served_ratio = np.array(load_data(folder_ratio, f"serving_ratio{j}")) 

            folder_generated = os.path.join(folder_path, f"generated_requests_over_simulation")
            generated_data = np.array(load_data(folder_generated, f"generated_requests_over_simulation{j}"))
            print(served_ratio)
            
            plt.plot(served_ratio[0])
            plt.show()
            served_data_flat = served_data.flatten()
            generated_data_flat = generated_data.flatten()

            served = np.concatenate((served, served_data_flat))
            generated = np.concatenate((generated, generated_data_flat))

        all_served_rl = np.concatenate((all_served_rl, served))
        all_generated_rl = np.concatenate((all_generated_rl, generated))

    episode_length_fifo = len(all_served_fifo) // 4
    average_points_fifo = [np.mean(all_served_fifo[i*episode_length_fifo:(i+1)*episode_length_fifo]) for i in range(4)]

    episode_length_rl = len(all_served_rl) // 4
    average_points_rl = [np.mean(all_served_rl[i*episode_length_rl:(i+1)*episode_length_rl]) for i in range(4)]
    print("Average served requests for RL:")
    for i, avg in enumerate(average_points_fifo, start=1):
        print(f"Episode {i}: {avg}")

    # Plotting the data
    # plt.figure(figsize=(10, 6))
    # plt.plot(all_served_fifo/all_generated_fifo)
    # plt.scatter(np.arange(episode_length_fifo, len(all_served_fifo)+1, episode_length_fifo), average_points_fifo, color='red', label='Average Served Requests')
    # plt.plot(np.arange(episode_length_fifo, len(all_served_fifo)+1, episode_length_fifo), average_points_fifo, color='red', linestyle='-', marker='o')

    # plt.plot(all_served_rl[3:]/all_generated_rl[3:-1])
    # print(all_served_rl)
    # plt.scatter(np.arange(episode_length_rl, len(all_served_rl)+1, episode_length_rl), average_points_rl, color='green', label='Average Served Requests')
    # plt.plot(np.arange(episode_length_rl, len(all_served_rl)+1, episode_length_rl), average_points_rl, color='green', linestyle='-', marker='o')
    
    # plt.xlabel('Time Step')
    # plt.ylabel('Served Requests')
    # plt.title('Served Requests Over Time')
    # plt.grid(True)
    # plt.legend()
    # plt.show()


if __name__ == "__main__":
    main()
