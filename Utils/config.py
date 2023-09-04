import random

import numpy as np

SERVICES_TYPES = {
    "ENTERTAINMENT": {
        "REALTIME": np.arange(start=7, stop=10),
        "BANDWIDTH": np.arange(start=8, stop=10 + 1),
        "CRITICAL": np.arange(start=5, stop=7 + 1),
    },
    "SAFETY": {
        "REALTIME": np.arange(start=9, stop=10),
        "BANDWIDTH": np.arange(start=6, stop=7 + 1),
        "CRITICAL": np.arange(start=9, stop=10 + 1),
    },
    "AUTONOMOUS": {
        "REALTIME": np.arange(start=9, stop=10),
        "BANDWIDTH": np.arange(start=7, stop=8 + 1),
        "CRITICAL": np.arange(start=8, stop=10 + 1),
    },
}

Grids = {
    "grid1": [],
    "grid2": [],
    "grid3": [],
    "grid4": [],
}

REALTIME_BANDWIDTH = {
    "Wifi": list(range(1, 3)),
    "ThreeG": list(range(3, 5)),
    "FourG": list(range(5, 7)),
    "FiveG": list(range(7, 9)),
    "Satellite": list(range(9, 10)),
}

CRITICAL_BANDWIDTH = {

}

outlet_types = {

    "3G": {
        "NUM_ANTENNAS": [2],
        "CHANNEL_BANDWIDTH": np.arange(1.5, 5, 0.25),
        "CODING_RATE": [1 / 2, 1 / 3],
        "MODULATION_ORDER": [4],
        "AVERAGE_SYMBOLS_PER_SLOT": np.arange(184, 200, 1),
        "NUM_SLOTS_PER_FRAME": [15],
        "NUM_FRAMES_PER_SECOND": [10],
    },
    "4G": {
        "NUM_ANTENNAS": [5, 6],
        "CHANNEL_BANDWIDTH": np.arange(15, 20, 0.5),
        "CODING_RATE": [1 / 2, 2 / 3, 3 / 4],
        "MODULATION_ORDER": [4, 6, 8],
        "AVERAGE_SYMBOLS_PER_SLOT": [18, 20],
        "NUM_SLOTS_PER_FRAME": [10],
        "NUM_FRAMES_PER_SECOND": [20],
    },
    "5G": {
        "NUM_ANTENNAS": [1],
        "CHANNEL_BANDWIDTH": np.arange(100, 200, 5),
        "CODING_RATE": [1 / 2, 2 / 3, 3 / 4, 4 / 5, 5 / 6],
        "MODULATION_ORDER": [4, 6, 8, 10],
        "AVERAGE_SYMBOLS_PER_SLOT": [12, 13, 14],
        "NUM_SLOTS_PER_FRAME": [10],
        "NUM_FRAMES_PER_SECOND": [60],
    },
    "wifi": {
        "NUM_ANTENNAS": [2],
        "CHANNEL_BANDWIDTH": np.arange(1.0, 5, 0.25),
        "CODING_RATE": [1 / 2, 1 / 3],
        "MODULATION_ORDER": [4],
        "AVERAGE_SYMBOLS_PER_SLOT": np.arange(100, 160, 1),
        "NUM_SLOTS_PER_FRAME": [10],
        "NUM_FRAMES_PER_SECOND": [8],
    }

}
