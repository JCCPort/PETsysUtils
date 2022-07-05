import numpy as np
import pandas as pd
import argparse

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
