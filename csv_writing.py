import csv
import os
import pickle

def read_pickle_file(file_path):
    objects = []
    with open(file_path, "rb") as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects

def save_metrics_as_csv(file_path_to_save, titles, metrics):
    if not os.path.exists(file_path_to_save):
        os.makedirs(file_path_to_save)

    for metric_name, data in metrics.items():
        csv_file_path = os.path.join(file_path_to_save, f"{metric_name}.csv")
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([titles.get(metric_name, metric_name)])
            for item in data:
                writer.writerow([item])

end_to_end_delay_file_path_fifo = os.path.join("run_fifo_scenario_3_lr_0.001", "end_to_end_delay", "end_to_end_delay0.pkl")
end_to_end_delay_file_path_rl = os.path.join("run_rl_scenario_3_lr_0.001", "end_to_end_delay", "end_to_end_delay0.pkl")

serving_ratio_file_path_fifo = os.path.join("run_fifo_scenario_3_lr_0.001", "serving_ratio", "serving_ratio0.pkl")
serving_ratio_file_path_rl = os.path.join("run_rl_scenario_3_lr_0.001", "serving_ratio", "serving_ratio0.pkl")

# Assuming read_pickle_file is defined elsewhere
end_to_end_delay_fifo = read_pickle_file(end_to_end_delay_file_path_fifo)
end_to_end_delay_rl = read_pickle_file(end_to_end_delay_file_path_rl)

serving_ratio_fifo = read_pickle_file(serving_ratio_file_path_fifo)
serving_ratio_rl = read_pickle_file(serving_ratio_file_path_rl)

metrics = {
    'end_to_end_delay_fifo': end_to_end_delay_fifo,
    'end_to_end_delay_rl': end_to_end_delay_rl,
    'serving_ratio_fifo': serving_ratio_fifo[0],
    'serving_ratio_rl': serving_ratio_rl[0]
}

titles = {
    'end_to_end_delay_fifo': 'End to End Delay FIFO',
    'end_to_end_delay_rl': 'End to End Delay RL',
    'serving_ratio_fifo': 'Serving Ratio Delay FIFO',
    'serving_ratio_rl': 'Serving Ratio Delay RL'
}

path_to_save_csv = './saved_csv/'

save_metrics_as_csv(path_to_save_csv, titles, metrics)
