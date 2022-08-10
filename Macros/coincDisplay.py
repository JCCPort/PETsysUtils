""" Plot the channels triggered in each coincidence group. First argument is the data file and the second file is the
mapping file. For optional arguments, see PETsys Logbook 10/08"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.patches as plt_p
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
    timeHistBins = np.arange(0, 160, 0.5)

    # setting up for optional arguments
    debug = False
    energyPlot = False
    cBarTopMin = None
    cBarTopMax = None
    ToT = True
    muon = False

    if len(sys.argv) > 3:
        if 'energy' in sys.argv:
            energyPlot = True
            print("Plotting energies, not hit count")
            fileName += '_energy'
        else:
            fileName += '_hits'

        if 'debug' in sys.argv:
            debug = True
            print("Debugging")

        if 'qdc' in sys.argv:
            ToT = False

        if 'muon' in sys.argv:
            muon = True
            fileName += '_muon'

    data = pd.DataFrame(data)
    # data = data[0:7]
    print("Length of data:", len(data))

    energyLimit = 0

    if debug:
        print(data[0:20])
    if energyPlot:
        cBarTopMin = data['energy'].min()
        cBarTopMax = data['energy'].max()
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

        # only working with the data in this group
        dataByGroup = data[data['group'] == group]
        summedEnergy = dataByGroup['energy'].sum()

        # cut in case of muons
        if summedEnergy < energyLimit:
            continue

        # add time wrt first in group. To show the first hit on the time heatmap, the time needs to not be 0.
        # Therefore all entries are offset by +1ns
        dataByGroup['timewrtfirst'] = ((dataByGroup['time'] - dataByGroup['time'].min()) / 1000) + 1

        # set colour bar limit for the time HM for the group
        cBarTimeMax = dataByGroup['timewrtfirst'].max()

        # separate into arrays
        chipID_4_data = dataByGroup[dataByGroup['array'] == 4]
        chipID_8_data = dataByGroup[dataByGroup['array'] == 8]

        # set up figure dimensions, titles and labels
        fig = plt.figure(figsize=(10, 13))

        if energyPlot:
            units = "ns"
            if not ToT:
                units = "a.u."
            titleEnergy = ", Total Energy = {:.4} {}".format(summedEnergy, units)
        else:
            titleEnergy = ""
        plt.suptitle("{}\nGroup {}".format(fileName, group) + titleEnergy)

        leftHM = fig.add_subplot(321)
        leftHM.set_xlabel('x [pixels]')
        leftHM.set_ylabel('y [pixels]')
        leftHM.title.set_text("ChipID = 4")
        leftHM.set_yticks(range(2, 7, 1))
        leftHM.set_xticks(range(2, 7, 1))

        rightHM = fig.add_subplot(322)
        rightHM.set_xlabel('x [pixels]')
        rightHM.set_ylabel('y [pixels]')
        rightHM.title.set_text("ChipID = 8")
        rightHM.set_yticks(range(2, 7, 1))
        rightHM.set_xticks(range(2, 7, 1))

        timeHM_left = fig.add_subplot(323)
        timeHM_left.set_xlabel('x [pixels]')
        timeHM_left.set_ylabel('y [pixels]')
        timeHM_left.title.set_text("ChipID = 4")
        timeHM_left.set_yticks(range(2, 7, 1))
        timeHM_left.set_xticks(range(2, 7, 1))

        timeHM_right = fig.add_subplot(324)
        timeHM_right.set_xlabel('x [pixels]')
        timeHM_right.set_ylabel('y [pixels]')
        timeHM_right.title.set_text("ChipID = 8")
        timeHM_right.set_yticks(range(2, 7, 1))
        timeHM_right.set_xticks(range(2, 7, 1))

        timePlot = fig.add_subplot(313)
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

        colourMap_white = ListedColormap("white")
        if chipID_4_data.shape[0] < 1:
            # cannot plot a blank entry => plot arbitrary data and colour is white...?
            h_left = leftHM.hist2d([2, 6], [2, 6], bins=[4, 4], range=[[2, 6], [2, 6]], cmin=1, cmap=colourMap_white,
                                   vmin=cBarTopMin, vmax=cBarTopMax)
            time_left = timeHM_left.hist2d([0, 0], [0, 1], bins=[4, 4], range=[[2, 6], [2, 6]], cmin=1,
                                           cmap=colourMap_white, vmax=cBarTimeMax, vmin=0)

        elif chipID_4_data.shape[0] < 2:
            # The function won't plot a grid for one data point, so we double it.
            # Need to compensate for this in the energy and time heatmaps by halving it
            temp_df_4 = pd.DataFrame(chipID_4_data)
            temp_df_4 = pd.concat([temp_df_4] * 2, ignore_index=True)
            if energyPlot:
                temp_weights_4 = temp_df_4['energy'] / 2
            else:
                temp_weights_4 = None

            h_left = leftHM.hist2d(temp_df_4['xi'], temp_df_4['yi'], bins=[4, 4], range=[[2, 6], [2, 6]],
                                   weights=temp_weights_4, cmin=1, vmin=cBarTopMin, vmax=cBarTopMax)
            time = timePlot.hist(chipID_4_data['timewrtfirst'], bins=timeHistBins, label="Chip 4")
            time_left = timeHM_left.hist2d(temp_df_4['xi'], temp_df_4['yi'], bins=[4, 4], range=[[2, 6], [2, 6]],
                                           weights=(temp_df_4['timewrtfirst']/2), cmin=1, vmax=cBarTimeMax, vmin=0,
                                           cmap=plt.cm.plasma_r)


        else:
            h_left = leftHM.hist2d(chipID_4_data['xi'], chipID_4_data['yi'], bins=[4, 4], range=[[2, 6], [2, 6]],
                                   weights=energyWeights_4, cmin=1, vmin=cBarTopMin, vmax=cBarTopMax)
            time = timePlot.hist(chipID_4_data['timewrtfirst'], bins=timeHistBins, label="Chip 4")
            time_left = timeHM_left.hist2d(chipID_4_data['xi'], chipID_4_data['yi'], bins=[4, 4],
                                           range=[[2, 6], [2, 6]], weights=chipID_4_data['timewrtfirst'], cmin=1,
                                           vmax=cBarTimeMax, vmin=0, cmap=plt.cm.plasma_r)

            if True in chipID_4_data['channel'].duplicated():
                txt = "Warning: Pixel receiving two hits in coincidence time window on array 4"
                plt.text(0.20, 0.92, txt, transform=fig.transFigure, size=12)
                print(chipID_4_data)

        if chipID_8_data.shape[0] < 1:
            h_right = rightHM.hist2d([2, 6], [2, 6], bins=[4, 4], range=[[2, 6], [2, 6]], cmin=1, cmap=colourMap_white,
                                     vmin=cBarTopMin, vmax=cBarTopMax)
            time_right = timeHM_right.hist2d([2, 6], [2, 6], bins=[4, 4], range=[[2, 6], [2, 6]], cmin=1,
                                             cmap=colourMap_white, vmin=0, vmax=cBarTimeMax)


        elif chipID_8_data.shape[0] < 2:
            temp_df_8 = pd.DataFrame(chipID_8_data)
            temp_df_8 = pd.concat([temp_df_8] * 2, ignore_index=True)
            if energyPlot:
                temp_weights_8 = temp_df_8['energy'] / 2
            else:
                temp_weights_8 = None

            h_right = rightHM.hist2d(temp_df_8['xi'], temp_df_8['yi'], bins=[4, 4], range=[[2, 6], [2, 6]],
                                     weights=temp_weights_8, cmin=1, vmin=cBarTopMin, vmax=cBarTopMax)
            time = timePlot.hist(chipID_8_data['timewrtfirst'], bins=timeHistBins, label="Chip 8")
            time_right = timeHM_right.hist2d(temp_df_8['xi'], temp_df_8['yi'], bins=[4, 4], range=[[2, 6], [2, 6]],
                                             weights=(temp_df_8['timewrtfirst']/2), vmin=0, vmax=cBarTimeMax,
                                             cmap=plt.cm.plasma_r, cmin=1)

        else:
            h_right = rightHM.hist2d(chipID_8_data['xi'], chipID_8_data['yi'], bins=[4, 4], range=[[2, 6], [2, 6]],
                                     weights=energyWeights_8, cmin=1, vmin=cBarTopMin, vmax=cBarTopMax)
            time = timePlot.hist(chipID_8_data['timewrtfirst'], bins=timeHistBins, label="Chip 8")
            time_right = timeHM_right.hist2d(chipID_8_data['xi'], chipID_8_data['yi'], bins=[4, 4],
                                             range=[[2, 6], [2, 6]], weights=chipID_8_data['timewrtfirst'], cmin=1,
                                             vmin=0, vmax=cBarTimeMax, cmap=plt.cm.plasma_r)
            if True in chipID_8_data['channel'].duplicated():
                txt = "Warning: Pixel receiving two hits in coincidence time window on array 8"
                plt.text(0.20, 0.94, txt, transform=fig.transFigure, size=12)
                print(chipID_8_data['channel'])

        # formatting plots
        # TODO: sort out order of formatting, we have some at beginning and some here
        leftHM.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1, alpha=0.5)
        rightHM.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1, alpha=0.5)
        timeHM_right.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1, alpha=0.5)
        timeHM_left.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1, alpha=0.5)

        leftHM.set_aspect('equal')
        rightHM.set_aspect('equal')
        timeHM_right.set_aspect('equal')
        timeHM_left.set_aspect('equal')

        timePlot.legend(loc="upper right")
        timePlot.ticklabel_format(axis='x', useOffset=True)

        # setting colour bars for the heatmaps
        if energyPlot:
            cbar_topLeft = fig.colorbar(h_left[3], ax=leftHM)
            cbar_topRight = fig.colorbar(h_right[3], ax=rightHM)
            if ToT:
                cbar_topLeft.set_label("Time over threshold [ns]")
                cbar_topRight.set_label("Time over threshold [ns]")
            else:
                cbar_topLeft.set_label("Energy [a.u.]")
                cbar_topRight.set_label("Energy [a.u.]")

        cbar_bottomLeft = fig.colorbar(time_left[3], ax=timeHM_left)
        cbar_bottomLeft.set_label("Time from first event [ns]")
        cbar_bottomRight = fig.colorbar(time_right[3], ax=timeHM_right)
        cbar_bottomRight.set_label("Time from first event [ns]")

        if debug:
            plt.show()
        else:
            pdf.savefig(fig)
        plt.close()

    if not debug:
        pdf.close()
    print("Complete")
