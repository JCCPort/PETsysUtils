import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Read petsys binary files')

parser.add_argument("-s", dest='signalName', type=str, required=True, help='Prefix filename of signal binary file')
parser.add_argument("-b", dest='bkgdName', type=str, required=True, help='Prefix filename of background binary file')
parser.add_argument('--range', dest='range', help='Range to plot over. If not included, will plot between [-10, 60]',
                    default=[0, 40], type=lambda s: [int(item) for item in s.split(',')])
parser.add_argument('--rangeSum', dest='rangeSum', help='Range to plot over. Default is [-5, 70]',
                    default=[-5, 70], type=lambda s: [int(item) for item in s.split(',')])
parser.add_argument("--bins", dest='bins', type=float, nargs='*', default=90,
                    help='Number of bins. If not included bins=100')
parser.add_argument("--binsSum", dest='binsSum', type=float, nargs='*', default=90,
                    help='Number of bins. If not included bins=100')
args = parser.parse_args()

# set as binary files
sFile = args.signalName + ".ldat"
bFile = args.bkgdName + ".ldat"

# set dataframes
dt = np.dtype([('mh_n1', np.byte),
               ('mh_j1', np.byte),
               ('time1', np.int64),
               ('energy1', np.float32),
               ('channelID1', np.int32),
               ('mh_n2', np.byte),
               ('mh_j2', np.byte),
               ('time2', np.int64),
               ('energy2', np.float32),
               ('channelID2', np.int32)])

dataSignal = np.fromfile(sFile, dtype=dt)
dataSignal = pd.DataFrame(dataSignal)

dataBkgd = np.fromfile(bFile, dtype=dt)
dataBkgd = pd.DataFrame(dataBkgd)

# extract energy data
energySignal1 = dataSignal['energy1']
energySignal2 = dataSignal['energy2']
energySignalSum = []
for i in range(len(energySignal1)):
    energySignalSum.append(energySignal1[i] + energySignal2[i])
energyBkgdSum = []
energyBkgd1 = dataBkgd['energy1']
energyBkgd2 = dataBkgd['energy2']
for i in range(len(energyBkgd1)):
    energyBkgdSum.append(energyBkgd1[1] + energyBkgd2[i])

# make histograms
histSigSum, edgesSum = np.histogram(energySignalSum, bins=np.linspace(args.rangeSum[0], args.rangeSum[1], args.binsSum))
histS1, edges = np.histogram(energySignal1, bins=np.linspace(args.range[0], args.range[1], args.bins))
histS2, edges = np.histogram(energySignal2, bins=np.linspace(args.range[0], args.range[1], args.bins))

histBkgdSum, edgesSum = np.histogram(energyBkgdSum, bins=np.linspace(args.rangeSum[0], args.rangeSum[1], args.binsSum))
histB1, edges = np.histogram(energyBkgd1, bins=np.linspace(args.range[0], args.range[1], args.bins))
histB2, edges = np.histogram(energyBkgd2, bins=np.linspace(args.range[0], args.range[1], args.bins))

leftEdges = edges[:-1]
leftEdgesSum = edgesSum[:-1]

# subtract histograms
histSubSum = histSigSum - histBkgdSum
histSub1 = histS1 - histB1
histSub2 = histS2 - histB2

plt.bar(leftEdgesSum, histSigSum, align='edge', label="test")
plt.title("Source-in: Sum")
plt.xlabel("Sum of energy [a.u.]")
plt.ylabel("Counts")
plt.show()

plt.bar(leftEdgesSum, histBkgdSum, align='edge', label="test")
plt.title("Background: Sum")
plt.xlabel("Sum of energy [a.u.]")
plt.ylabel("Counts")
plt.show()

plt.bar(leftEdgesSum, histSubSum, align='edge', label="test")
plt.title("Background subtracted: Sum")
plt.xlabel("Sum of energy [a.u.]")
plt.ylabel("Counts")
plt.show()

plt.bar(leftEdges, histSub1, align='edge')
plt.title("Background subtracted: Higher energy events")
plt.xlabel("Energy [a.u.]")
plt.ylabel("Counts")
plt.show()

plt.bar(leftEdges, histSub2, align='edge')
plt.title("Background subtracted: Lower energy events")
plt.xlabel("Energy [a.u.]")
plt.ylabel("Counts")
plt.show()

plt.bar(leftEdges, histS1, align='edge')
plt.title("Source-in: Higher energy events")
plt.xlabel("Energy [a.u.]")
plt.ylabel("Counts")
plt.show()

plt.bar(leftEdges, histS2, align='edge')
plt.title("Source-in: Lower energy events")
plt.xlabel("Energy [a.u.]")
plt.ylabel("Counts")
plt.show()

plt.bar(leftEdges, histB1)
plt.title("Background: Higher energy events")
plt.xlabel("Energy [a.u.]")
plt.ylabel("Counts")
plt.show()

plt.bar(leftEdges, histB2)
plt.title("Background: Lower energy events")
plt.xlabel("Energy [a.u.]")
plt.ylabel("Counts")
plt.show()
