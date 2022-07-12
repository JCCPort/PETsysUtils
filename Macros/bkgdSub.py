""" Energy distribution background subtraction script for PETsys singles binary files
 Written by E. Bannister and J. Lock at University of Sussex July 2022 """

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

# read in arguments
parser = argparse.ArgumentParser(description='Read petsys binary files')

parser.add_argument("-s", dest='signalName', type=str, required=True, help='Prefix filename of signal binary file')
parser.add_argument("-b", dest='bkgdName', type=str, required=True, help='Prefix filename of background binary file')
parser.add_argument("--channel", dest='channel', type=int,
                    help='Channel to look at. If not included, all channels will be plotted')
parser.add_argument('--range', dest='range', help='Range to plot over. If not included, will plot between [-10, 60]',
                    default=[-10, 40], type=lambda s: [int(item) for item in s.split(',')])
parser.add_argument("--bins", dest='bins', type=int, default=300,
                    help='Number of bins. If not included bins=100')

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
histS, edgesS = np.histogram(energySignal, bins=np.linspace(args.range[0], args.range[1], args.bins))
leftEdgesS = edgesS[:-1]

histB, edgesB = np.histogram(energyBkgd, bins=np.linspace(args.range[0], args.range[1], args.bins))
leftEdgesB = edgesB[:-1]

# subtract histograms
histSub = histS - histB

# format histograms
plt.bar(leftEdgesS, histSub, align='edge', label="test")
plt.title("Background Subtracted")
plt.xlabel("Energy [a.u.]")
plt.ylabel("Counts")
plt.show()

plt.bar(leftEdgesS, histS, align='edge')
plt.title("Source-in")
plt.xlabel("Energy [a.u.]")
plt.ylabel("Counts")
plt.show()

plt.bar(leftEdgesB, histB)
plt.title("Background")
plt.xlabel("Energy [a.u.]")
plt.ylabel("Counts")
plt.show()
print(len(energySignal))
print(len(energyBkgd))
print(len(histB))
