import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    data = np.fromfile(sys.argv[1], dtype=[("time", np.longlong),
                                                                                               ("energy", np.single),
                                                                                               ("channel", np.intc),
                                                                                               ("group", np.int64)])

    data = pd.DataFrame(data)
    #print(data[0:30])
    groupSumEnergies = data.groupby('group')['energy'].sum().reset_index()['energy'].values
    print(len(groupSumEnergies))
    #print(np.min(groupSumEnergies), np.max(groupSumEnergies))
    #print(groupSumEnergies)
    # groupSumEnergies = groupSumEnergies[groupSumEnergies < 1e4]
    plt.hist(groupSumEnergies, bins=500, label="80 ns window, majority 5")
    #plt.xlim([-2, 20])
    plt.ylabel("Counts")
    plt.xlabel("Sum energy")
    plt.title(sys.argv[1].split("/")[-1])
    plt.legend()
    plt.tight_layout()
    plt.show()
