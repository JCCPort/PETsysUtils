import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import argparse
import struct

# parse arguments
parser = argparse.ArgumentParser( \
    description='Read petsys binary files and make make background subtraction')
parser.add_argument("-s", dest='signalName', type=str, required=True, \
                    help='Prefix filename of signal binary file')
parser.add_argument("-b", dest='bkgdName', type=str, required=True, \
                    help='Prefix filename of background binary file')

# parser.add_argument('--channel',type=int, \
#                     help='Channel to plot the energy distribution of. \
# #         If not included all channels will be plotted')
# parser.add_argument('--step1',type=float,help='Value of step1 to plot. \
#         If not included all step1 values will be plotted')
# parser.add_argument('--step2',type=float,help='Value of step2 to plot. \
#         If not included all step2 values will be plotted')
# parser.add_argument('--step1Title',type=str,default="Step1", \
#                     help='Title of step1 parameter')
# parser.add_argument('--step2Title',type=str,default="Step2", \
#                     help='Title of step2 parameter')

args = parser.parse_args()

sFile = args.signalName + ".ldat"  # binary file containing data
bFile = args.bkgdName + ".ldat"  # binary file containing data


dtS = np.dtype([('time', np.int64), ('energy', np.float32), ('channelID', np.int32)])
dataS = np.fromfile(sFile, dtype=dtS)
dataSignal = pd.DataFrame(dataS)

dtB = np.dtype([('time', np.int64), ('energy', np.float32), ('channelID', np.int32)])
dataB = np.fromfile(bFile, dtype=dtB)
dataBkgd = pd.DataFrame(dataB)


# extract energy data from specified channel if given
energySignal = dataSignal['energy']
energyBkgd = dataBkgd['energy']

print(energySignal)
print(energyBkgd)

# hist(energy,bins=5000,range=[-10,900])
# enDist.set_xlim([-10,200])
# enDist.ticklabel_format(axis='y',style='sci',scilimits=(-3,4))
#
# plt.savefig(args.fileName+".pdf")
# plt.show()
#
# print(5)
