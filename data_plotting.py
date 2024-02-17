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
                        data.append(pickle.load(f))
                    except EOFError:
                        break
    return data

def plot_fifo(folder_paths, title):
    plt.figure(figsize=(12, 6))

    # Initialize arrays to store data from all FIFO runs
    all_aborted = []
    all_rejected = []
    all_timed_out = []
    all_generated = []

    for folder_path in folder_paths:
        # Temporary arrays to store data from current FIFO run
        aborted = []
        rejected = []
        timed_out = []
        generated = []

        for j in range(4):
            folder_aborted = os.path.join(folder_path, f"number_of_abort_requests_over_the_simulation")
            aborted.extend(load_data(folder_aborted, f"number_of_abort_requests_over_the_simulation{j}"))

            folder_rejected = os.path.join(folder_path, f"number_of_rejected_requests_over_simulation")
            rejected.extend(load_data(folder_rejected, f"number_of_rejected_requests_over_simulation{j}"))

            folder_timed_out = os.path.join(folder_path, f"number_of_timed_out_requests_from_algorithm")
            timed_out.extend(load_data(folder_timed_out, f"number_of_timed_out_requests_from_algorithm{j}"))

            folder_generated = os.path.join(folder_path, f"generated_requests_over_simulation")
            generated.extend(load_data(folder_generated, f"generated_requests_over_simulation{j}"))

        # Concatenate data from current FIFO run to the arrays storing data from all FIFO runs
        all_aborted.extend(aborted)
        all_rejected.extend(rejected)
        all_timed_out.extend(timed_out)
        all_generated.extend(generated)

    max_length = max(len(all_generated), len(all_aborted), len(all_rejected), len(all_timed_out))

    all_aborted = np.pad(all_aborted, (0, max_length - len(all_aborted)), mode='constant')
    all_rejected = np.pad(all_rejected, (0, max_length - len(all_rejected)), mode='constant')
    all_timed_out = np.pad(all_timed_out, (0, max_length - len(all_timed_out)), mode='constant')
    all_generated = np.pad(all_generated, (0, max_length - len(all_generated)), mode='constant')

    differences = all_generated - all_aborted - all_rejected - all_timed_out

    plt.plot(differences, label=title)
    plt.xlabel('Simulation Index')
    plt.ylabel('Difference')
    plt.title("FIFO Runs")
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    fifo_folder_paths = [f"run_fifo_just_on_rush_hours_lr_0.001_0{i}" for i in range(3, 5)]
    plot_fifo(fifo_folder_paths, "FIFO")

if __name__ == "__main__":
    main()
