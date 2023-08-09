import os
from Environment.utils.paths import prev_centralize_weights_path#,prev_decentralize_weights_path , prev_decentralize_memory_path

def load_weigths_buffer(gridcell):
    for i in range(1):
        #self.gridcells_dqn[i]
        gridcell.model.load_weights(
            os.path.join(prev_centralize_weights_path, f"weights_0.hdf5")
        )
        # self.gridcells_dqn[i].agents.fill_memory(self.gridcells_dqn[i].agents.memory , os.path.join(prev_centralize_memory_path, f'centralize_buffer.pkl'))
    for i in range(1):
        print()
        # for index, outlet in enumerate(gridcell.agents.grid_outlets):
        #     outlet.dqn.model.load_weights(os.path.join(prev_decentralize_weights_path, f'weights_1.hdf5'))
        #     outlet.dqn.agents.fill_memory(outlet.dqn.agents.memory , os.path.join(prev_decentralize_memory_path, f'decentralize_buffer{index}.pkl'))
        #     print("..............")
        # print("out : ",gridcell.agents.grid_outlets[0].__class__.__name__)
        # print("weights2 : ")
        # print("out : ", gridcell.agents.grid_outlets[1].__class__.__name__)
        # print("weights1 : ")
        # print("out : ", gridcell.agents.grid_outlets[2].__class__.__name__)
        # print("weights0 : ")
        # gridcell.agents.grid_outlets[0].dqn.model.load_weights(os.path.join(prev_decentralize_weights_path, f'weights_2.hdf5'))
        # gridcell.agents.grid_outlets[1].dqn.model.load_weights(os.path.join(prev_decentralize_weights_path, f'weights_1.hdf5'))
        # gridcell.agents.grid_outlets[2].dqn.model.load_weights(os.path.join(prev_decentralize_weights_path, f'weights_0.hdf5'))
        #
        #
        # gridcell.agents.grid_outlets[0].dqn.agents.fill_memory(gridcell.agents.grid_outlets[0].dqn.agents.memory ,
        #                                                        os.path.join(prev_decentralize_memory_path, f'decentralize_buffer2.pkl'))
        # gridcell.agents.grid_outlets[1].dqn.agents.fill_memory(gridcell.agents.grid_outlets[1].dqn.agents.memory ,
        #                                                        os.path.join(prev_decentralize_memory_path, f'decentralize_buffer1.pkl'))
        # gridcell.agents.grid_outlets[2].dqn.agents.fill_memory(gridcell.agents.grid_outlets[2].dqn.agents.memory,
        #                                                        os.path.join(prev_decentralize_memory_path,
        #                                                                     f'decentralize_buffer0.pkl'))



