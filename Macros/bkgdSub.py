import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Read petsys binary files')

parser.add_argument("-s", dest='signalName', type=str, required=True, help='Prefix filename of signal binary file')
parser.add_argument("-b", dest='bkgdName', type=str, required=True, help='Prefix filename of background binary file')
parser.add_argument("--channel", dest='channel', type=int,
                    help='Channel to look at. If not included, all channels will be plotted')
parser.add_argument("--range", dest='range', type=float, nargs='*', default=[-10, 500],
                    help='Range to plot over. If not included, will plot between [-10, 500]')
parser.add_argument("--bins", dest='bins', type=float, nargs='*', default=10000,
                    help='Number of bins. If not included bins=10000')

args = parser.parse_args()

# set as binary files
sFile = args.signalName + ".ldat"
bFile = args.bkgdName + ".ldat"

# set dataframes
dt = np.dtype([('time', np.int64), ('energy', np.float32), ('channelID', np.int32)])

dataSignal = np.fromfile(sFile, dtype=dt)
dataSignal = pd.DataFrame(dataSignal)

dataBkgd = np.fromfile(bFile, dtype=dt)
dataBkgd = pd.DataFrame(dataBkgd)

if args.channel:
    dataSignal = dataSignal.loc[dataSignal['channelID'] == args.channel]
    dataBkgd = dataBkgd.loc[dataBkgd['channelID'] == args.channel]

# extract energy data
energySignal = dataSignal['energy']
energyBkgd = dataBkgd['energy']

# make histograms
histS, edgesS = np.histogram(energySignal, bins=np.linspace(0, 50, 300))
leftEdgesS = edgesS[:-1]
width = 1 * (leftEdgesS[1] - leftEdgesS[0])

histB, edgesB = np.histogram(energyBkgd, bins=np.linspace(0, 50, 300))
leftEdgesB = edgesB[:-1]

# subtract histograms
histSub = histS - histB

plt.bar(leftEdgesS, histSub, align='edge', width=width)
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
