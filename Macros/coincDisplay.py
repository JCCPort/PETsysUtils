""" Plot the channels triggered in each coincidence group. First argument is the data file and the second file is the
mapping file"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as plt_p
import matplotlib.backends.backend_pdf as b_pdf
from matplotlib.colors import ListedColormap

if __name__ == '__main__':
    # read in data
    data = np.fromfile(sys.argv[1], dtype=[("time", np.longlong), ("energy", np.single), ("channel", np.intc),
                                           ("group", np.int64)])
    # read in channel mapping info
    mapFile = pd.read_csv(sys.argv[2], sep='\t', header=None,
                          names=['portID', 'slaveID', 'chipID', 'channelID', 'regionID', 'xi', 'yi', 'x', 'y', 'z'])

    # misc variables for formatting/debugging/testing
    fileName = sys.argv[1].split("/")[-1].split(".ldat")[0]
    pd.options.mode.chained_assignment = None
    tempTimeHistLimit = 1000000
    timeHistBins = np.arange(0, 160, 0.25)

    # choice for energy plotting goes after mapping file, otherwise debug and energy plot goes anyway
    debug = False
    energyPlot = False
    cBarMin = None
    cBarMax = None
    ToT = True
    muon = False

    if len(sys.argv) > 3:
        if 'energy' in sys.argv:
            energyPlot = True
            print("Plotting energies, not hit count")

        if 'debug' in sys.argv:
            debug = True
            print("Debugging")

        if 'qdc' in sys.argv:
            ToT = False

        if 'muon' in sys.argv:
            muon = True
            fileName += '_muon'

    data = pd.DataFrame(data)
    data = data[0:2500]
    print("Length of data:", len(data))
    energyLimit = data['energy'].max() + 1

    if debug:
        # print("Length of data:", len(data))
        print(data[0:20])
    if energyPlot:
        cBarMin = data['energy'].min()
        cBarMax = data['energy'].max()
    if muon:
        energyLimit = 2000

    groupEnergy = data.groupby('group')['energy'].sum().reset_index()['energy'].values

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
        pdf = b_pdf.PdfPages("../tempFigureDump/display_{}.pdf".format(fileName))
        # firstPage = plt.figure(figsize=(11.69, 8.27))
        # firstPage.clf()
        # txt = 'This is not all the events in this run, it is cut due to \n' \
        #       'processing time. The last group may not have all hits and\n' \
        #       'therefore should be discarded.'
        # firstPage.text(0.5, 0.5, txt, transform=firstPage.transFigure, size=24, ha="center")
        # pdf.savefig()
        # plt.close()
    else:
        pdf = None

    for group in range(0, max_group + 1):
        if group % 10 == 0:
            print("Group {} of {}".format(group, max_group))

        dataByGroup = data[data['group'] == group]
        summedEnergy = dataByGroup['energy'].sum()

        if summedEnergy < energyLimit:
            continue

        # separate into arrays
        chipID_4_data = dataByGroup[dataByGroup['array'] == 4]
        chipID_8_data = dataByGroup[dataByGroup['array'] == 8]

        # add time wrt first in group
        firstEvent = dataByGroup['time'].min()
        chipID_4_data['timewrtfirst'] = (chipID_4_data['time'] - firstEvent) / 1000

        chipID_8_data['timewrtfirst'] = (chipID_8_data['time'] - firstEvent) / 1000

        # set up figure
        fig = plt.figure(figsize=(12, 10))

        if not energyPlot:
            plotType = "Location of hits in coincidence window"
        else:
            plotType = "Location of hits (weighted by ToT) in coincidence window"
        plt.suptitle("Run: {}\n{}\nGroup {}".format(fileName, plotType, group))

        leftHM = fig.add_subplot(221)
        leftHM.set_xlabel('x [pixels]')
        leftHM.set_ylabel('y [pixels]')
        leftHM.title.set_text("ChipID = 4")

        rightHM = fig.add_subplot(222)
        rightHM.set_xlabel('x [pixels]')
        rightHM.set_ylabel('y [pixels]')
        rightHM.title.set_text("ChipID = 8")

        timePlot = fig.add_subplot(212)
        timePlot.set_xlabel('Time from first event in group [ns]')
        timePlot.set_ylabel('Count')
        timePlot.set_yticks(range(0, 6, 1))

        # optional energy weights
        if energyPlot:
            energyWeights_4 = chipID_4_data['energy']
            energyWeights_8 = chipID_8_data['energy']
        else:
            energyWeights_4 = None
            energyWeights_8 = None


        # plotting the heatmaps
        # getting around not plotting <2 on an array
        # fix does not account for the two events being on the same channel
        # TODO: Either figure out how to do this properly, or get the colours sorted at the very least
        colourMap_white = ListedColormap("white")

        if chipID_4_data.shape[0] < 1:
            h_left = leftHM.hist2d([0, 0], [0, 1], bins=[8, 8], range=[[0, 8], [0, 8]], cmin=1, cmap=colourMap_white,
                                   vmin=cBarMin, vmax=cBarMax)

        elif chipID_4_data.shape[0] < 2:
            # The function won't plot a grid for one data point, so we double it. Need to compensate for this in the energy plot
            temp_df_4 = pd.DataFrame(chipID_4_data)
            temp_df_4 = pd.concat([temp_df_4] * 2, ignore_index=True)
            if energyPlot:
                temp_weights_4 = temp_df_4['energy'] / 2
            else:
                temp_weights_4 = None

            h_left = leftHM.hist2d(temp_df_4['xi'], temp_df_4['yi'], bins=[8, 8], range=[[0, 8], [0, 8]],
                                   weights=temp_weights_4, cmin=1, vmin=cBarMin, vmax=cBarMax)
            time = timePlot.hist(chipID_4_data['timewrtfirst'], bins=timeHistBins, label="Chip 4")

            # txt = chipID_4_data['timewrtfirst']
            # plt.text(0.10, 0.47, txt, transform=fig.transFigure, size=12)
        else:
            h_left = leftHM.hist2d(chipID_4_data['xi'], chipID_4_data['yi'], bins=[8, 8], range=[[0, 8], [0, 8]],
                                   weights=energyWeights_4, cmin=1, vmin=cBarMin, vmax=cBarMax)
            time = timePlot.hist(chipID_4_data['timewrtfirst'], bins=timeHistBins, label="Chip 4")

        if chipID_8_data.shape[0] < 1:
            h_right = rightHM.hist2d([0, 0], [0, 1], bins=[8, 8], range=[[0, 8], [0, 8]], cmin=1, cmap=colourMap_white,
                                     vmin=cBarMin, vmax=cBarMax)

        elif chipID_8_data.shape[0] < 2:

            temp_df_8 = pd.DataFrame(chipID_8_data)
            temp_df_8 = pd.concat([temp_df_8] * 2, ignore_index=True)
            if energyPlot:
                temp_weights_8 = temp_df_8['energy'] / 2
            else:
                temp_weights_8 = None

            # txt = str(temp_df_8)
            # plt.text(0.65, 0.47, txt, transform=fig.transFigure, size=12)

            h_right = rightHM.hist2d(temp_df_8['xi'], temp_df_8['yi'], bins=[8, 8], range=[[0, 8], [0, 8]],
                                     weights=temp_weights_8, cmin=1, vmin=cBarMin, vmax=cBarMax)
            time = timePlot.hist(chipID_8_data['timewrtfirst'], bins=timeHistBins, label="Chip 8")

        else:
            h_right = rightHM.hist2d(chipID_8_data['xi'], chipID_8_data['yi'], bins=[8, 8], range=[[0, 8], [0, 8]],
                                     weights=energyWeights_8, cmin=1, vmin=cBarMin, vmax=cBarMax)
            time = timePlot.hist(chipID_8_data['timewrtfirst'], bins=timeHistBins, label="Chip 8")

        # formatting plots
        leftHM.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1, alpha=0.5)
        rightHM.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1, alpha=0.5)

        leftHM.set_aspect('equal')
        rightHM.set_aspect('equal')

        leftHM.add_patch(plt_p.Rectangle((2, 2), 4, 4, facecolor=(0, 0, 0, 0), edgecolor='r', linewidth=2))
        rightHM.add_patch(plt_p.Rectangle((2, 2), 4, 4, facecolor=(0, 0, 0, 0), edgecolor='r', linewidth=2))

        timePlot.legend(loc="upper right")
        timePlot.ticklabel_format(axis='x', useOffset=True)

        if energyPlot:
            cbar_left = fig.colorbar(h_left[3], ax=leftHM)
            cbar_right = fig.colorbar(h_right[3], ax=rightHM)
            if ToT:
                cbar_left.set_label("Time over threshold [ns]")
                cbar_right.set_label("Time over threshold [ns]")

        if debug:
            plt.show()
        else:
            pdf.savefig(fig)
        plt.close()

    if not debug:
        pdf.close()
    print("Complete")
