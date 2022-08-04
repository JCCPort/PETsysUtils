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
    plt.hist(data['energy'], bins=300)
    plt.ylabel('counts')
    plt.xlabel('energy')
    plt.title('Raw energy {}'.format(sys.argv[1].split("/")[-1]))
    plt.show()
    #print(data[0:30])
    #data['energy'] = data['energy'][data['energy']>30]
    groupSumEnergies = data.groupby('group')['energy'].sum().reset_index()['energy'].values
    print(len(groupSumEnergies))
    #print(np.min(groupSumEnergies), np.max(groupSumEnergies))
    #print(groupSumEnergies)
    # groupSumEnergies = groupSumEnergies[groupSumEnergies < 1e4]
    plt.hist(groupSumEnergies, bins=200, label="Mean:\t\t{:.2f}\nStdDev:\t\t{:.2f}".format(np.mean(groupSumEnergies), np.std(groupSumEnergies)).expandtabs())
    #plt.xlim([-10, 50])
    plt.ylabel("Counts")
    plt.xlabel("Sum energy")
    plt.yscale('log')
    plt.title("Sum energy {}".format(sys.argv[1].split("/")[-1]))
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.hist(groupSumEnergies, bins=200, label="Mean:\t\t{:.2f}\nStdDev:\t\t{:.2f}".format(np.mean(groupSumEnergies), np.std(groupSumEnergies)).expandtabs())
    #plt.xlim([-10, 50])
    plt.ylabel("Counts")
    plt.xlabel("Sum energy")
    #plt.yscale('log')
    plt.title("Sum energy {}".format(sys.argv[1].split("/")[-1]))
    plt.legend()
    plt.tight_layout()
    plt.show()
