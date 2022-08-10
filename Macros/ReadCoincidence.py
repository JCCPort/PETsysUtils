import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    data = np.fromfile(sys.argv[1],
                       dtype=[("time", np.longlong), ("energy", np.single), ("channel", np.intc), ("group", np.int64)])

    if len(sys.argv) == 2:
        histLabel = None
    else:
        histLabel = "{}".format(sys.argv[2])
        print("Argument after file path reserved for histogram label or 'debug'")

    # Each coincidence group has energies summed
    data = pd.DataFrame(data)
    groupSumEnergies = data.groupby('group')['energy'].sum().reset_index()['energy'].values

    # groupSumEnergies = groupSumEnergies[groupSumEnergies < 1e4]

    # Data debug
    if sys.argv[2] == "debug":
        print("DEBUG")
        print("First 10 entries: \n", data[0:10])
        print("Length of data:", len(data))
        print("Length of groupSumEnergies:", len(groupSumEnergies))
        print("groupSumEnergies min = {}, max = {}".format(np.min(groupSumEnergies), np.max(groupSumEnergies)))

    plt.hist(groupSumEnergies, bins=500, label=histLabel)
    # plt.xlim([-2, 20])
    plt.ylabel("Counts")
    plt.xlabel("Sum energy")
    #plt.yscale('log')
    plt.title("Sum energy {}".format(sys.argv[1].split("/")[-1]))
    plt.legend()
    plt.tight_layout()
    plt.show()
