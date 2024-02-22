import os
import pickle
import numpy as np

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
    served_requests_folder = os.path.join(folder_path, "served_requests_over_simulation")
    os.makedirs(served_requests_folder, exist_ok=True)
    file_path = os.path.join(served_requests_folder, f"served_requests_{j}.pkl")
    with open(file_path, "wb") as f:
        pickle.dump(served_requests, f)

def save_folders(folder_paths, title):
    for folder_path in folder_paths:
        for j in range(0, 4):
            all_aborted = []
            all_rejected = []
            all_timed_out = []
            all_generated = []

            folder_aborted = os.path.join(folder_path, f"number_of_abort_requests_over_the_simulation")
            all_aborted.extend(load_data(folder_aborted, f"number_of_abort_requests_over_the_simulation{j}"))

            folder_rejected = os.path.join(folder_path, f"number_of_rejected_requests_over_simulation")
            all_rejected.extend(load_data(folder_rejected, f"number_of_rejected_requests_over_simulation{j}"))

            folder_timed_out = os.path.join(folder_path, f"number_of_timed_out_requests_from_algorithm")
            all_timed_out.extend(load_data(folder_timed_out, f"number_of_timed_out_requests_from_algorithm{j}"))

            folder_generated = os.path.join(folder_path, f"generated_requests_over_simulation")
            all_generated.extend(load_data(folder_generated, f"generated_requests_over_simulation{j}"))

            max_length = max(len(all_generated), len(all_aborted), len(all_rejected), len(all_timed_out))

            all_aborted = np.pad(all_aborted, (0, max_length - len(all_aborted)), mode='constant')
            all_rejected = np.pad(all_rejected, (0, max_length - len(all_rejected)), mode='constant')
            all_timed_out = np.pad(all_timed_out, (0, max_length - len(all_timed_out)), mode='constant')
            all_generated = np.pad(all_generated, (0, max_length - len(all_generated)), mode='constant')

            served_requests = all_generated - all_aborted - all_rejected - all_timed_out
            save_served_requests(folder_path, j, served_requests)

def main():
    fifo_folder_paths = [f"run_rl_just_on_rush_hours_lr_0.001_{i}" for i in range(97,98)]
    save_folders(fifo_folder_paths, "FIFO")

if __name__ == "__main__":
    main()
