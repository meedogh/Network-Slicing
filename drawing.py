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
      ranged_values_fifo = np.arange(0, len(end_to_end_delay_fifo))
      ranged_values_rl = np.arange(0, len(end_to_end_delay_rl))      
      ranged_values_serving_fifo = np.arange(0, len(serving_ratio_fifo))
      ranged_values_serving_rl = np.arange(0, len(serving_ratio_rl))

      if plot_type == 'all':
            fig, ax = plt.subplots(number_of_plots, number_of_plots, figsize=(5*number_of_plots, 2*number_of_plots))
            ax[0][0].plot(ranged_values_fifo, end_to_end_delay_fifo)
            ax[0][0].set_xlabel('Steps')
            ax[0][0].set_ylabel('end to end delay fifo')

            ax[1][0].plot(ranged_values_rl, end_to_end_delay_rl)
            ax[1][0].set_xlabel('Steps')
            ax[1][0].set_ylabel('end to end delay rl')
            
            # ax[0].set_title(f'{end_to_end_title}')

            ax[0][1].plot(ranged_values_serving_fifo, serving_ratio_fifo)
            ax[0][1].set_xlabel('Steps')
            ax[0][1].set_ylabel('serving ratio delay fifo')

            ax[1][1].plot(ranged_values_serving_rl, serving_ratio_rl)
            ax[1][1].set_xlabel('Steps')
            ax[1][1].set_ylabel('serving ratio delay rl')
      
      elif plot_type == 'multiple':
            fig, ax = plt.subplots(number_of_plots, figsize=(5*number_of_plots, 2*number_of_plots))
            if len(end_to_end_delay_fifo)>0:
                  ax[0].plot(ranged_values_fifo, end_to_end_delay_fifo)
                  ax[0].set_xlabel('Steps')
                  ax[0].set_ylabel('end to end delay fifo')
                  ax[0].set_title(f'{end_to_end_title}')
            if len(end_to_end_delay_rl):
                  ax[1].plot(ranged_values_rl, end_to_end_delay_rl)
                  ax[1].set_xlabel('Steps')
                  ax[1].set_ylabel('end to end delay rl')
                  ax[1].set_title(f'{end_to_end_title}')
            if len(serving_ratio_fifo):
                  ax[0].plot(ranged_values_serving_fifo, serving_ratio_fifo)
                  ax[0].set_xlabel('Steps')
                  ax[0].set_ylabel('serving ratio delay fifo')
                  ax[0].set_title(f'{serving_ratio_title}')

            if len(serving_ratio_rl):
                  ax[1].plot(ranged_values_serving_rl, serving_ratio_rl)
                  ax[1].set_xlabel('Steps')
                  ax[1].set_ylabel('serving ratio delay rl')
                  ax[1].set_title(f'{serving_ratio_title}')

            
      elif plot_type == 'in_one':
            fig, ax = plt.subplot()
            legend_list = []
            if len(serving_ratio_fifo)>0:
                  ax.plot(ranged_values_serving_fifo,serving_ratio_fifo)
                  legend_list.append('serving ratio fifo')
            
            if len(serving_ratio_rl)>0:
                  ax.plot(ranged_values_serving_rl,serving_ratio_rl)
                  legend_list.append('serving ratio rl')
            
            if len(end_to_end_delay_fifo)>0:
                  ax.plot(ranged_values_fifo,end_to_end_delay_fifo)
                  legend_list.append('end to end delay fifo')
            
            if len(end_to_end_delay_rl)>0:
                  ax.plot(ranged_values_rl,end_to_end_delay_rl)
                  legend_list.append('end to end delay rl')
            ax.legend(legend_list)
            ax.set_title(f'{main_title}')
            

      # ax[1].set_title(f'{serving_ratio_title}')
      plt.savefig(f'{file_path_to_save+main_title}.jpg')
      plt.savefig(f'{file_path_to_save+main_title}.svg')
      plt.tight_layout()
      plt.show()

end_to_end_delay_file_path_fifo = "run_fifo_scenario_1_lr_0.001//end_to_end_delay//end_to_end_delay0.pkl"
end_to_end_delay_fifo = read_pickle_file(end_to_end_delay_file_path_fifo)
end_to_end_delay_file_path_rl = "run_rl_scenario_1_lr_0.001//end_to_end_delay//end_to_end_delay0.pkl"
end_to_end_delay_rl = read_pickle_file(end_to_end_delay_file_path_rl)

serving_ratio_file_path_fifo = "run_fifo_scenario_1_lr_0.001//serving_ratio//serving_ratio0.pkl"
serving_ratio_fifo = read_pickle_file(serving_ratio_file_path_fifo)
serving_ratio_file_path_rl = "run_rl_scenario_1_lr_0.001//serving_ratio//serving_ratio0.pkl"
serving_ratio_rl = read_pickle_file(serving_ratio_file_path_rl)



metrics = {}
titles = {}

titles['main_title'] = 'comparision between metrics'
titles['end_to_end_title'] = 'end to end delay comparision'
titles['serving_ratio_title'] = 'serving ratio delay comparision'

metrics['end_to_end_delay_fifo'] = end_to_end_delay_fifo
metrics['end_to_end_delay_rl'] = end_to_end_delay_rl
metrics['serving_ratio_fifo'] = serving_ratio_fifo[0]
metrics['serving_ratio_rl'] = serving_ratio_rl[0]

path_to_save_plots = './/saved_plots//'

if not os.path.exists(path_to_save_plots):
      os.mkdir(path_to_save_plots)

plot_metrics(titles=titles,
            number_of_plots=2,
            file_path_to_save=path_to_save_plots,
            metrics=metrics,
            plot_type='all')


