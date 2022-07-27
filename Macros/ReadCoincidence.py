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
    groupSumEnergies = data.groupby('group')['energy'].sum().reset_index()['energy'].values
    groupSumEnergies = groupSumEnergies[groupSumEnergies < 1e4]
    plt.hist(groupSumEnergies, bins=300, label="80 ns window, majority 2")
    # plt.xlim([0, 200])
    plt.ylabel("Counts")
    plt.xlabel("Sum energy")
    plt.title("run5_LED_qdc_single_sorted_grouped.ldat")
    plt.legend()
    plt.tight_layout()
    plt.show()
