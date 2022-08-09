""" Plot the channels triggered in each coincidence group. First argument is the data file and the second file is the
mapping file"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as plt_p
import matplotlib.backends.backend_pdf
from matplotlib.colors import ListedColormap

if __name__ == '__main__':
    data = np.fromfile(sys.argv[1], dtype=[("time", np.longlong), ("energy", np.single), ("channel", np.intc),
                                           ("group", np.int64)])

    fileName = sys.argv[1].split("/")[-1].split(".ldat")[0]
    pd.options.mode.chained_assignment = None
    tempTimeHistLimit = 1000000
    timeHistBins = range(0, 100000, 100)

    # debug option as an argument after the map channel
    debug = False
    energyPlot = False
    if len(sys.argv) > 3:
        if (sys.argv[3] == 'debug') or (sys.argv[4] == 'debug'):
            debug = True
            print("Debugging")
        if sys.argv[3] == 'energy':
            energyPlot = True
            print("Plotting energies, not hit count")

    data = pd.DataFrame(data)
    # data_limit = int(len(data)/700)
    # data = data[0:20]

    if debug:
        print("Length of data:", len(data))
        print(data[0:20])

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
    else:
        pdf = None

    for group in range(0, max_group + 1):
        if group % 100 == 0:
            print("Group {} of {}".format(group, max_group))
        dataByGroup = data[data['group'] == group]

        # separate into arrays
        chipID_4_data = dataByGroup[dataByGroup['array'] == 4]
        chipID_8_data = dataByGroup[dataByGroup['array'] == 8]

        # add time wrt first in group
        firstEvent = dataByGroup['time'].min()
        chipID_4_data['timewrtfirst'] = chipID_4_data['time'] - firstEvent

        chipID_8_data['timewrtfirst'] = chipID_8_data['time'] - firstEvent

        # set up figure
        fig = plt.figure(figsize=(10, 10))
        plt.suptitle("Run: {}\nGroup {}".format(fileName, group))

        leftHM = fig.add_subplot(221)
        leftHM.set_xlabel('x [pixels]')
        leftHM.set_ylabel('y [pixels]')
        leftHM.title.set_text("ChipID = 4")

        rightHM = fig.add_subplot(222)
        rightHM.set_xlabel('x [pixels]')
        rightHM.set_ylabel('y [pixels]')
        rightHM.title.set_text("ChipID = 8")

        timePlot = fig.add_subplot(212)

        # plotting the heatmaps
        # getting around not plotting <2 on an array
        # fix does not account for the two events being on the same channel
        # TODO: Either figure out how to do this properly, or get the colours sorted at the very least
        colourMap_white = ListedColormap("white")

        if chipID_4_data.shape[0] < 1:
            h_left = leftHM.hist2d([0, 0], [0, 1], bins=[8, 8], range=[[0, 8], [0, 8]], cmin=1, cmap=colourMap_white)
            # print(chipID_4_data)
        elif chipID_4_data.shape[0] < 2:
            temp_df_4 = pd.DataFrame(chipID_4_data)
            temp_df_4 = pd.concat([temp_df_4] * 2, ignore_index=True)
            h_left = leftHM.hist2d(temp_df_4['xi'], temp_df_4['yi'], bins=[8, 8], range=[[0, 8], [0, 8]], cmin=1)
            time = timePlot.hist(chipID_4_data['timewrtfirst'], bins=timeHistBins, label="Chip 4")

            # txt = chipID_4_data['timewrtfirst']
            # plt.text(0.10, 0.47, txt, transform=fig.transFigure, size=12)

        else:
            h_left = leftHM.hist2d(chipID_4_data['xi'], chipID_4_data['yi'], bins=[8, 8], range=[[0, 8], [0, 8]],
                                   cmin=1)
            time = timePlot.hist(chipID_4_data['timewrtfirst'], bins=timeHistBins, label="Chip 4")

        if chipID_8_data.shape[0] < 1:
            h_right = rightHM.hist2d([0, 0], [0, 1], bins=[8, 8], range=[[0, 8], [0, 8]], cmin=1, cmap=colourMap_white)
            # print(chipID_8_data)
        elif chipID_8_data.shape[0] < 2:
            temp_df_8 = pd.DataFrame(chipID_8_data)
            temp_df_8 = pd.concat([temp_df_8] * 2, ignore_index=True)
            h_right = rightHM.hist2d(temp_df_8['xi'], temp_df_8['yi'], bins=[8, 8], range=[[0, 8], [0, 8]], cmin=1)
            time = timePlot.hist(chipID_8_data['timewrtfirst'], bins=timeHistBins, label="Chip 8")

            # txt = str(chipID_8_data['timewrtfirst'])
            # plt.text(0.65, 0.47, txt, transform=fig.transFigure, size=12)
        else:
            h_right = rightHM.hist2d(chipID_8_data['xi'], chipID_8_data['yi'], bins=[8, 8], range=[[0, 8], [0, 8]],
                                     cmin=1)
            time = timePlot.hist(chipID_8_data['timewrtfirst'], bins=timeHistBins, label="Chip 8")

        # formatting plots
        leftHM.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1, alpha=0.5)
        rightHM.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1, alpha=0.5)

        leftHM.set_aspect('equal')
        rightHM.set_aspect('equal')

        leftHM.add_patch(plt_p.Rectangle((2, 2), 4, 4, facecolor=(0, 0, 0, 0), edgecolor='r', linewidth=2))
        rightHM.add_patch(plt_p.Rectangle((2, 2), 4, 4, facecolor=(0, 0, 0, 0), edgecolor='r', linewidth=2))

        timePlot.legend(loc="upper right")
        # timePlot.set_xlim([0, 100000])
        timePlot.ticklabel_format(axis='x', useOffset=True)

        print("Group", group)
        print(chipID_4_data)
        print(chipID_8_data)
        print("\n")

        if debug:
            plt.show()
        else:
            pdf.savefig(fig)
        plt.close()

    if not debug:
        pdf.close()
    print("Complete")
