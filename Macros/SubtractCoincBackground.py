"""Takes two arguments: signal run and a background run, both having had the Sussex coincidence filtering applied.
Performs background subtraction of the summed energies of groups histograms"""

import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == '__main__':
    print("Signal run:", sys.argv[1].split("/")[-1], "\nBackground run:", sys.argv[2].split("/")[-1])

    signal = np.fromfile(sys.argv[1], dtype=[("time", np.longlong), ("energy", np.single), ("channel", np.intc),
                                             ("group", np.int64)])
    background = np.fromfile(sys.argv[2], dtype=[("time", np.longlong), ("energy", np.single), ("channel", np.intc),
                                                 ("group", np.int64)])

    # Sum energy in a coincidence group
    signal = pd.DataFrame(signal)
    sigGroupEnergy = signal.groupby('group')['energy'].sum().reset_index()['energy'].values

    background = pd.DataFrame(background)
    bkgdGroupEnergy = background.groupby('group')['energy'].sum().reset_index()['energy'].values

    histRange = [min([min(sigGroupEnergy), min(bkgdGroupEnergy)]), max([max(sigGroupEnergy), max(bkgdGroupEnergy)])]
    numBins = 1000
    # print(bkgdGroupEnergy)
    # print(histRange)

    # print(sigGroupEnergy[0:10])
    # print(len(sigGroupEnergy))
    # print(len(bkgdGroupEnergy))
    # print(sigGroupEnergy)


    histSignal, binSig = np.histogram(sigGroupEnergy, np.linspace(histRange[0], histRange[1]), numBins)
    histBackground, binBkgd = np.histogram(bkgdGroupEnergy, np.linspace(histRange[0], histRange[1]), numBins)

    histSub = histSignal - histBackground
    plt.bar(binSig[:-1], histSub, width=(binSig[3]-binSig[2]))
    plt.title("Signal: {},\nBackground: {}".format(sys.argv[1].split("/")[-1].split("_single")[0], sys.argv[2].split("/")[-1].split("_single")[0]))
    plt.ylabel("Signal - Background Difference")
    plt.xlabel("Group Sum Energy")
    plt.show()
