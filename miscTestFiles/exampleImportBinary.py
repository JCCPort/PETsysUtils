""" Use as a template at the start of scripts to read in binary files """

import numpy as np
import pandas as pd
import argparse

# read in data
parser = argparse.ArgumentParser(description='Read petsys binary files')

parser.add_argument("-o", dest='fileName', type=str, required=True, help='Prefix filename of signal binary file')
parser.add_argument("--channel", dest='channel', type=int, help='Channel to look at. If not included, all channels '
                                                                'will be plotted')

args = parser.parse_args()
file = args.fileName + ".ldat"

# turn into pandas dataframe
dt = np.dtype([('time', np.int64), ('energy', np.float32), ('channelID', np.int32)])
data = np.fromfile(file, dtype=dt)
data = pd.DataFrame(data)

if args.channel:
    data = data.loc[data['channelID'] == args.channel]
