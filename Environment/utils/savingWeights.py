import os
from .paths import path_memory_decentralize,path_memory_centralize ,centralized_weights ,decentralized_weights

def save_weigths_buffer(gridcell):
    for index, outlet in enumerate(gridcell.agents.grid_outlets):
        outlet.dqn.model.save_weights(os.path.join(decentralized_weights, f"weights_{index}.hdf5"))
        outlet.dqn.agents.free_up_memory(
            outlet.dqn.agents.memory,
            os.path.join(
                path_memory_decentralize, f"decentralize_buffer{index}.pkl"
            ),
        )
    # for i in range(1):
    #     print()
    # gridcell.model.save_weights(os.path.join(centralized_weights, f'weights_{i}.hdf5'))
    # gridcell.agents.free_up_memory(self.gridcells_dqn[i].agents.memory , os.path.join(path_memory_centralize, f'centralize_buffer.pkl'))

    # shutil.copytree(results_dir, prev_results_dir)
