import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt

# parse arguments
parser = argparse.ArgumentParser(description='Read petsys binary files')

parser.add_argument("-s", dest='signalName', type=str, required=True, help='Prefix filename of signal binary file')
parser.add_argument("-b", dest='bkgdName', type=str, required=True, help='Prefix filename of background binary file')

args = parser.parse_args()

sFile = args.signalName + ".ldat"  # binary file containing data
bFile = args.bkgdName + ".ldat"  # binary file containing data

# set dataframes
dtS = np.dtype([('time', np.int64), ('energy', np.float32), ('channelID', np.int32)])
dataS = np.fromfile(sFile, dtype=dtS)
dataSignal = pd.DataFrame(dataS)

dtB = np.dtype([('time', np.int64), ('energy', np.float32), ('channelID', np.int32)])
dataB = np.fromfile(bFile, dtype=dtB)
dataBkgd = pd.DataFrame(dataB)

# extract energy data
energySignal = dataSignal['energy']
energyBkgd = dataBkgd['energy']

# make histograms
histS, edgesS = np.histogram(energySignal, bins=np.linspace(0,50,300))
leftEdgesS = edgesS[:-1]
width = 1*(leftEdgesS[1] - leftEdgesS[0])

histB, edgesB = np.histogram(energyBkgd, bins=np.linspace(0,50,300))
leftEdgesB = edgesB[:-1]

# subtract histograms
histSub = histS - histB

plt.bar(leftEdgesS, histSub, align='edge',width=width)
plt.title("Background subtracted")
plt.show()

plt.bar(leftEdgesS, histS, align='edge', width=width)
plt.title("Source-in")
plt.show()

plt.bar(leftEdgesB, histB)
plt.title("Background")
plt.show()
print(len(energySignal))
print(len(energyBkgd))
