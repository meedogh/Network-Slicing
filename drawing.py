import pickle
import os
import matplotlib.pyplot as plt
import numpy as np

def read_pickle_file(file_path):
      objects = []
      with (open(file_path, "rb")) as openfile:
            while True:
                  try:
                        objects.append(pickle.load(openfile))
                  except EOFError:
                        break
      return objects

def plot_metrics(*, titles, number_of_plots, file_path_to_save, metrics, plot_type):
      if not os.path.exists(file_path_to_save):
            os.mkdir(file_path_to_save)
      main_title = titles['main_title']
      end_to_end_title = titles['end_to_end_title']
      serving_ratio_title = titles['serving_ratio_title']
      end_to_end_delay_fifo = metrics['end_to_end_delay_fifo']
      end_to_end_delay_rl = metrics['end_to_end_delay_rl']
      serving_ratio_fifo = metrics['serving_ratio_fifo']
      serving_ratio_rl = metrics['serving_ratio_rl']
      # time_out_delay_fifo = metrics['time_out_delay_fifo']
      time_out_delay_rl = metrics['time_out_delay_rl']
      ranged_values_fifo = np.arange(0, len(end_to_end_delay_fifo))
      ranged_values_rl = np.arange(0, len(end_to_end_delay_rl))      
      ranged_values_serving_fifo = np.arange(0, len(serving_ratio_fifo))
      ranged_values_serving_rl = np.arange(0, len(serving_ratio_rl))

      if plot_type == 'all':
            fig, axs = plt.subplots(number_of_plots, number_of_plots, figsize=(5*number_of_plots, 2*number_of_plots))
            axs[0][0].plot(ranged_values_fifo, end_to_end_delay_fifo)
            axs[0][0].set_xlabel('Num Requests')
            axs[0][0].set_ylabel('End to End Delay FIFO')

            axs[1][0].plot(ranged_values_rl, end_to_end_delay_rl)
            axs[1][0].set_xlabel('Num Requests')
            axs[1][0].set_ylabel('End to End Delay RL')
            
            axs[0][1].set_title(f'{end_to_end_title}')

            axs[0][1].plot(ranged_values_serving_fifo, serving_ratio_fifo)
            axs[0][1].set_xlabel('Num Requests')
            axs[0][1].set_ylabel('serving ratio fifo')

            axs[1][1].plot(ranged_values_serving_rl, serving_ratio_rl)
            axs[1][1].set_xlabel('Num Requests')
            axs[1][1].set_ylabel('serving ratio rl')
      
      elif plot_type == 'multiple':
            fig, ax = plt.subplots(number_of_plots, figsize=(5*number_of_plots, 2*number_of_plots))
            if len(end_to_end_delay_fifo)>0:
                  ax.plot(ranged_values_fifo, end_to_end_delay_fifo, linewidth=2.5)
                  ax.set_xlabel('Steps', fontsize=12)
                  ax.set_ylabel('End to End Delay', fontsize=12)
                  ax.set_title(f'{end_to_end_title}', fontsize=12, fontweight='bold')
            # if len(end_to_end_delay_rl):
            #       ax[1].plot(ranged_values_rl, end_to_end_delay_rl)
            #       ax[1].set_xlabel('Num Requests')
            #       ax[1].set_ylabel('End to End Delay RL')
            #       ax[1].set_title(f'{end_to_end_title}')
            # if len(serving_ratio_fifo):
            #       ax[0].plot(ranged_values_serving_fifo, serving_ratio_fifo)
            #       ax[0].set_xlabel('Num Requests')
            #       ax[0].set_ylabel('serving ratio delay fifo')
            #       ax[0].set_title(f'{serving_ratio_title}')

            # if len(serving_ratio_fifo):
            #       ax.plot(ranged_values_serving_fifo, serving_ratio_fifo)
            #       ax.set_xlabel('Steps', fontsize = 12)
            #       ax.set_ylabel('Serving Ratio', fontsize = 12)
            #       ax.set_title(f'{serving_ratio_title}', fontsize = 12, fontweight='bold')

            
      elif plot_type == 'in_one':
            ax = plt.subplot()
            legend_list = []
            # if len(serving_ratio_fifo)>0:
            #       ax.plot(ranged_values_serving_fifo,serving_ratio_fifo)
            #       legend_list.append('serving ratio fifo')
            
            # if len(serving_ratio_rl)>0:
            #       ax.plot(ranged_values_serving_rl,serving_ratio_rl)
            #       legend_list.append('serving ratio rl')
            
            if len(end_to_end_delay_rl)>0:
                  print("X")
                  ax.plot(ranged_values_rl,end_to_end_delay_rl)
                  legend_list.append('end to end delay rl')
            if len(time_out_delay_rl)>0:
                  ax.plot(ranged_values_rl,time_out_delay_rl)
                  legend_list.append('time out rl')
            
            # if len(end_to_end_delay_rl)>0:
            #       ax.plot(ranged_values_rl,end_to_end_delay_rl)
            #       legend_list.append('end to end delay rl')
            ax.legend(legend_list)
            ax.set_title(f'{main_title}')
            

      # ax[1].set_title(f'{serving_ratio_title}')
      plt.savefig(f'{file_path_to_save+main_title}.jpg')
      plt.savefig(f'{file_path_to_save+main_title}.svg')
      plt.tight_layout()
      plt.show()
      
end_to_end_delay_file_path_fifo = os.path.join("run_fifo_scenario_2_lr_0.001", "end_to_end_delay", "end_to_end_delay0.pkl")
end_to_end_delay_file_path_rl = os.path.join("run_rl_scenario_2_lr_0.001", "end_to_end_delay", "end_to_end_delay0.pkl")

serving_ratio_file_path_fifo = os.path.join("run_fifo_scenario_2_lr_0.001", "serving_ratio", "serving_ratio0.pkl")
serving_ratio_file_path_rl = os.path.join("run_rl_scenario_2_lr_0.001", "serving_ratio", "serving_ratio0.pkl")

time_out_delay_file_path_rl = os.path.join("run_rl_scenario_2_lr_0.001", "time_out_delay", "time_out_delay0.pkl")
# Assuming read_pickle_file is defined elsewhere
end_to_end_delay_fifo = read_pickle_file(end_to_end_delay_file_path_fifo)
end_to_end_delay_rl = read_pickle_file(end_to_end_delay_file_path_rl)

serving_ratio_fifo = read_pickle_file(serving_ratio_file_path_fifo)
serving_ratio_rl = read_pickle_file(serving_ratio_file_path_rl)

time_out_delay_rl = read_pickle_file(time_out_delay_file_path_rl)



metrics = {}
titles = {}

titles['main_title'] = 'comparision between metrics'
titles['end_to_end_title'] = 'End to End Delay Scenario 2 RL'
titles['serving_ratio_title'] = 'Serving Ratio Scenario 2 RL'

metrics['end_to_end_delay_fifo'] = end_to_end_delay_fifo
metrics['end_to_end_delay_rl'] = end_to_end_delay_rl
metrics['serving_ratio_fifo'] = serving_ratio_fifo[0]
metrics['serving_ratio_rl'] = serving_ratio_rl[0]
# metrics['time_out_delay_fifo'] = time_out_delay_fifo
metrics['time_out_delay_rl'] = time_out_delay_rl

path_to_save_plots = './/saved_plots//'

if not os.path.exists(path_to_save_plots):
      os.mkdir(path_to_save_plots)

plot_metrics(titles=titles,
            number_of_plots=2,
            file_path_to_save=path_to_save_plots,
            metrics=metrics,
            plot_type='all')


