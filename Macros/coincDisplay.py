""" Plot the channels triggered in each coincidence group. First argument is the data file and the second file is the
mapping file"""
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as plt_p
import matplotlib.backends.backend_pdf

if __name__ == '__main__':
    data = np.fromfile(sys.argv[1], dtype=[("time", np.longlong), ("energy", np.single), ("channel", np.intc),
                                           ("group", np.int64)])

    fileName = sys.argv[1].split("/")[-1].split(".ldat")[0]

    # debug option as an argument after the map channel
    debug = False
    if len(sys.argv) == 4:
        if sys.argv[3] == 'debug':
            debug = True
            print("Debugging")

    data = pd.DataFrame(data)
    data_limit = int(len(data)/700)
    data = data[0:data_limit]

    if debug:
        print("Length of data:", len(data))
        print(data[0:10])

    groupEnergy = data.groupby('group')['energy'].sum().reset_index()['energy'].values

    # read in channel mapping info
    mapFile = pd.read_csv(sys.argv[2], sep='\t', header=None,
                          names=['portID', 'slaveID', 'chipID', 'channelID', 'regionID', 'xi', 'yi', 'x', 'y', 'z'])

    # calculate absolute channel IDs and add to mapping dataframe
    mapFile['absChID'] = mapFile['chipID'] * 64 + mapFile['channelID']

    # map the channel ID to the coordinates given in the mapping file
    data['xi'] = data['channel'].map(mapFile.set_index('absChID')['xi'])
    data['yi'] = data['channel'].map(mapFile.set_index('absChID')['yi'])

    # add column for which SiPM array it occurs on
    data['array'] = data['channel'].map(mapFile.set_index('absChID')['chipID'])

    # event by event basis
    max_group = data['group'].max()

    # open pdf to save figures
    if not debug:

        pdf = matplotlib.backends.backend_pdf.PdfPages("../tempFigureDump/output_{}.pdf".format(fileName))

    for i in range(0, max_group):
        if i % 100 == 0:
            print("Group {} of {}".format(i, max_group))
        dataByGroup = data[data['group'] == i]

        # separate into arrays
        chipID_4_data = dataByGroup[dataByGroup['array'] == 4]
        chipID_8_data = dataByGroup[dataByGroup['array'] == 8]

        if len(chipID_4_data) < 2:
            warnings.warn("Group skipped, cannot plot <2 events on an array")
            continue
        if len(chipID_8_data) < 2:
            warnings.warn("Group skipped, cannot plot <2 events on an array")
            continue

        # set up plots
        fig = plt.figure(figsize=(10, 10))
        plt.suptitle("Run: {}".format(fileName))

        # textPlot = fig.add_subplot(223)
        # textPlot.text(0,0, "test")

        leftHM = fig.add_subplot(221)
        leftHM.set_xlabel('x [pixels]')
        leftHM.set_ylabel('y [pixels]')
        leftHM.title.set_text("ChipID = 4")

        rightHM = fig.add_subplot(222)
        rightHM.set_xlabel('x [pixels]')
        rightHM.set_ylabel('y [pixels]')
        rightHM.title.set_text("ChipID = 8")

        h_left = leftHM.hist2d(chipID_4_data['xi'], chipID_4_data['yi'], bins=[8, 8], range=[[0, 8], [0, 8]], cmin=1)
        leftHM.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1, alpha=0.5)

        h_right = rightHM.hist2d(chipID_8_data['xi'], chipID_8_data['yi'], bins=[8, 8], range=[[0, 8], [0, 8]], cmin=1)
        rightHM.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1, alpha=0.5)

        leftHM.set_aspect('equal')
        rightHM.set_aspect('equal')

        leftHM.add_patch(plt_p.Rectangle((2, 2), 4, 4, facecolor=(0, 0, 0, 0), edgecolor='r', linewidth=2))
        rightHM.add_patch(plt_p.Rectangle((2, 2), 4, 4, facecolor=(0, 0, 0, 0), edgecolor='r', linewidth=2))

        # txt = str(chipID_4_data)
        # plt.text(0.09, 0.35, txt, transform=fig.transFigure, size=12)

        if debug:
            plt.show()

        if not debug:
            pdf.savefig(fig)
            plt.close()

    if not debug:
        pdf.close()
    print("Complete")
