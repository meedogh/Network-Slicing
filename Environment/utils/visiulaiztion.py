import os

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from .paths import utility_requested_ensured_path,reward_decentralized_path,reward_centralized_path,\
    qvalue_decentralized_path,qvalue_centralized_path,reward_320_decentralized_path

matplotlib.use('agg')


def plotting_Utility_Requested_Ensured():
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(100, 52))
    fig.subplots_adjust(hspace=0.8)
    lines_out_utility = []
    lines_out_requested = []
    lines_out_ensured = []
    j = 0
    out=['wifi','3G','4G']
    for i in range(1):
        row = 0
        line, line1, line2 = 0, 0, 0
        for index in range(3):
            if index == 0:
                color_str = 'b'
            elif index == 1:
                color_str = 'r'
            elif index == 2:
                color_str = 'g'
            line, = axs.flatten()[j].plot([], [], label=f"{out[index]} utility", color=color_str )
            line1, = axs.flatten()[j + 1].plot([], [], label=f"{out[index]} requested", color=color_str)
            line2, = axs.flatten()[j + 2].plot([], [], label=f"{out[index]} ensured", color=color_str )
            lines_out_utility.append(line)
            lines_out_requested.append(line1)
            lines_out_ensured.append(line2)
        j += 3

    return fig, axs, lines_out_utility, lines_out_requested, lines_out_ensured


def plotting_Qvalue_decentralize():
    fig_Qvalue_decentralize, axs_Qvalue_decentralize = plt.subplots(nrows=1, ncols=3, figsize=(100, 120))
    fig_Qvalue_decentralize.subplots_adjust(hspace=0.8)
    lines_out_Qvalue_decentralize = []
    for i, ax in enumerate(axs_Qvalue_decentralize.flatten()):
        line, = ax.plot([], [], label=f"O{i + 1} qvalue", color='b')
        lines_out_Qvalue_decentralize.append(line)
    return fig_Qvalue_decentralize, axs_Qvalue_decentralize, lines_out_Qvalue_decentralize


def update_lines_Qvalue_decentralized(lines_out_Qvalue_decentralize, steps, outlet):
    for j, line3 in enumerate(lines_out_Qvalue_decentralize):
        # print("outlet[j].qvalue", outlet[j].qvalue)

        x_data, y_data = line3.get_data()
        x_data = np.append(x_data, steps)

        y_data = np.append(y_data, outlet[j].qvalue)
        line3.set_data(x_data, y_data)


def plotting_Qvalue_centralize():
    fig_Qvalue_centralize, axs_Qvalue_centralize = plt.subplots(figsize=(100, 52))
    lines_out_Qvalue_centralize, = axs_Qvalue_centralize.plot([], [], label="grid qvalue", color='b')
    return fig_Qvalue_centralize, axs_Qvalue_centralize, [lines_out_Qvalue_centralize]

def plotting_reward_decentralize():
    fig_reward_decentralize, axs_reward_decentralize = plt.subplots(nrows=1, ncols=3, figsize=(100, 120))
    fig_reward_decentralize.subplots_adjust(hspace=0.8)
    lines_out_reward_decentralize = []
    for i, ax in enumerate(axs_reward_decentralize.flatten()):
        line, = ax.plot([], [], label=f"O{i + 1} reward", color='b',marker='o')
        lines_out_reward_decentralize.append(line)
    return fig_reward_decentralize, axs_reward_decentralize, lines_out_reward_decentralize

def plotting_reward_320_decentralize():
    fig_reward_320_decentralize, axs_reward_320_decentralize = plt.subplots(nrows=1, ncols=3, figsize=(100, 120))
    fig_reward_320_decentralize.subplots_adjust(hspace=0.8)
    lines_out_reward_320_decentralize = []
    for i, ax in enumerate(axs_reward_320_decentralize.flatten()):
        line, = ax.plot([], [], label=f"O{i + 1} reward", color='b',marker='o')
        lines_out_reward_320_decentralize.append(line)
    return fig_reward_320_decentralize, axs_reward_320_decentralize, lines_out_reward_320_decentralize



# def plotting_reward_centralize():
#     fig_reward_centralize, axs_reward_centralize = plt.subplots(nrows=1, ncols=1, figsize=(100, 52))
#     fig_reward_centralize.subplots_adjust(hspace=0.8)
#     lines_out_reward_centralize = []
#
#     for i, ax in enumerate(axs_reward_centralize.flatten()):
#         line, = ax.plot([], [], label=f"grid{i + 1} reward", color='b')
#         lines_out_reward_centralize.append(line)
#     return fig_reward_centralize, axs_reward_centralize , lines_out_reward_centralize


def plotting_reward_centralize():
    fig_reward_centralize, ax_reward_centralize = plt.subplots(figsize=(100, 52))
    line, = ax_reward_centralize.plot([], [], label="grid reward", color='b')
    return fig_reward_centralize, ax_reward_centralize, [line]


def update_lines_outlet_utility(lines_out_utility, steps, outlets):
    for j, line in enumerate(lines_out_utility):
        x_data, y_data = line.get_data()
        x_data = np.append(x_data, steps)
        y_data = np.append(y_data, outlets[j].dqn.environment.reward.utility)
        line.set_data(x_data, y_data)



def update_lines_outlet_requested(lines_out_requested, steps, outlets):
    for j, line1 in enumerate(lines_out_requested):
        x_data, y_data = line1.get_data()
        x_data = np.append(x_data, steps)
        y_data = np.append(y_data, outlets[j].dqn.environment.reward.service_requested)
        line1.set_data(x_data, y_data)


def update_lines_outlet_ensured(lines_out_ensured, steps, outlets):
    for j, line2 in enumerate(lines_out_ensured):
        x_data, y_data = line2.get_data()
        x_data = np.append(x_data, steps)
        y_data = np.append(y_data, outlets[j].dqn.environment.reward.service_ensured)
        line2.set_data(x_data, y_data)


def update_lines_reward_decentralized(lines_out_reward_decentralize, steps, outlets):
    for j, line3 in enumerate(lines_out_reward_decentralize):
        x_data, y_data = line3.get_data()
        x_data = np.append(x_data, steps)

        # print("outlets[j].dqn.environment.reward.rolling_sum_reward : ", outlets[j].dqn.environment.reward.rolling_sum_reward)
        y_data = np.append(y_data, outlets[j].dqn.environment.reward.rolling_sum_reward)
        line3.set_data(x_data, y_data)

def update_lines_reward_320_decentralized(lines_out_reward_decentralize, steps, outlets):
    for j, line3 in enumerate(lines_out_reward_decentralize):
        x_data, y_data = line3.get_data()
        x_data = np.append(x_data, steps)

        # print("outlets[j].dqn.environment.reward.rolling_sum_reward : ", outlets[j].dqn.environment.reward.rolling_sum_reward)
        y_data = np.append(y_data, outlets[j].dqn.environment.reward.rolling_sum_reward_320)
        line3.set_data(x_data, y_data)

def update_lines_reward_centralized(lines_out_reward_centralize, steps, gridcells_dqn):

    for j, line4 in enumerate(lines_out_reward_centralize):
        x_data, y_data = line4.get_data()
        x_data = np.append(x_data, steps)
        y_data = np.append(y_data, gridcells_dqn.environment.reward.reward_value)
        line4.set_data(x_data, y_data)
def update_lines_Qvalue_centralized(lines_out_Qvalue_centralize, steps, qvalue):
    # print("befor plotting ")
    for j, line4 in enumerate(lines_out_Qvalue_centralize):
        # print("after plotting ",qvalue)
        x_data, y_data = line4.get_data()
        x_data = np.append(x_data, steps)
        y_data = np.append(y_data, qvalue)
        line4.set_data(x_data, y_data)



fig_reward_decentralize, axs_reward_decentralize, lines_out_reward_decentralize = plotting_reward_decentralize()
fig_reward_centralize, axs_reward_centralize, lines_out_reward_centralize = plotting_reward_centralize()
fig, axs, lines_out_utility, lines_out_requested, lines_out_ensured = plotting_Utility_Requested_Ensured()
fig_Qvalue_decentralize, axs_Qvalue_decentralize, lines_out_Qvalue_decentralize = plotting_Qvalue_decentralize()
fig_Qvalue_centralize, axs_Qvalue_centralize, lines_out_Qvalue_centralize = plotting_Qvalue_centralize()
fig_reward_320_decentralize, axs_reward_320_decentralize, lines_out_reward_320_decentralize = plotting_reward_320_decentralize()



def take_snapshot_figures():
    for axs_ in [axs, axs_Qvalue_centralize,axs_reward_decentralize,axs_reward_320_decentralize,
                 axs_Qvalue_decentralize]:
        if hasattr(axs_, 'flatten'):
            for ax in axs_.flatten():
                ax.legend()
                ax.grid(True)
                ax.relim()
                ax.autoscale_view()
        else:
            axs_.legend()
            axs_.relim()
            axs_.autoscale_view()

    if axs is axs:
        fig.canvas.draw()
    elif axs is axs_Qvalue_centralize:
        axs_Qvalue_centralize.canvas.draw()
    elif axs is axs_Qvalue_decentralize:
        axs_Qvalue_decentralize.canvas.draw()

    path1 = os.path.join(utility_requested_ensured_path, f'snapshot')
    path2 = os.path.join(reward_decentralized_path, f'snapshot')
    path3 = os.path.join(reward_centralized_path, f'snapshot')
    path4 = os.path.join(qvalue_decentralized_path, f'snapshot')
    path5 = os.path.join(qvalue_centralized_path, f'snapshot')
    path6 = os.path.join(reward_320_decentralized_path, f'snapshot')
    fig.set_size_inches(10, 8)
    fig_reward_centralize.set_size_inches(15, 10)
    fig_reward_decentralize.set_size_inches(30, 20)  # set physical size of plot in inches
    fig_Qvalue_centralize.set_size_inches(15, 10)
    fig_Qvalue_decentralize.set_size_inches(30, 20)
    fig_reward_320_decentralize.set_size_inches(30, 20)
    fig.savefig(path1 + '.svg', dpi=300)
    fig_reward_decentralize.savefig(path2 + '.svg', dpi=300)
    # fig.savefig(path3 + '.svg', dpi=300)
    fig_Qvalue_decentralize.savefig(path4 + '.svg', dpi=300)
    fig_Qvalue_centralize.savefig(path5 + '.svg', dpi=300)
    fig_reward_320_decentralize.savefig(path6 + '.svg', dpi=300)

def update_figures(steps,temp_outlets,gridcells_dqn):
    update_lines_outlet_utility(lines_out_utility, steps, temp_outlets)
    update_lines_outlet_requested(lines_out_requested, steps, temp_outlets)
    update_lines_outlet_ensured(lines_out_ensured, steps, temp_outlets)
    # update_lines_Qvalue_decentralized(lines_out_Qvalue_decentralize, steps, temp_outlets)
    update_lines_reward_decentralized(lines_out_reward_decentralize, steps, temp_outlets)
    # update_lines_reward_centralized(lines_out_reward_centralize, steps, gridcells_dqn[0])
    # update_lines_Qvalue_centralized(lines_out_Qvalue_centralize, steps, gridcells_dqn[0].agents.qvalue
    #                                 )

def close_figures():
    plt.close(fig)
    plt.close(fig_Qvalue_centralize)
    plt.close(fig_Qvalue_decentralize)
    plt.close(fig_reward_decentralize)
    plt.close(fig_reward_320_decentralize)


