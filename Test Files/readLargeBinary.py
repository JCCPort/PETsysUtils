""" This works fine for certain sizes, but does not fulfill it's intended purpose """
# Todo(Jess): Get this working?

import pandas as pd
import numpy as np
import argparse


def read_in_chunks(file_object, chunk_size=1024):
    """ Reads in a binary file chunk by chunk, taken from stackoverflow.com/questions/519633"""

    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


# parse arguments
parser = argparse.ArgumentParser(description='Read large petsys binary files')

parser.add_argument("-s", dest='fileName', type=str, required=True)
args = parser.parse_args()

# set as binary files
file = args.fileName + ".ldat"

# open each chunk and write to dataframe
dt = np.dtype([('time', np.int64), ('energy', np.float32), ('channelID', np.int32)])

f = open(file, 'rb')
data = []
count = 0
for piece in read_in_chunks(f):
    piece = np.frombuffer(piece, dtype=dt)
    for i in range(0, len(piece)):
        oneEvent = []
        for j in range(0, 3):
            oneEvent.append(piece[i][j])
        data.append(oneEvent)
    count += 1
    print("Chunk {} Loaded".format(count))
f.close()

data = pd.DataFrame(data, columns=['time', 'energy', 'channelID'])

print(data)
