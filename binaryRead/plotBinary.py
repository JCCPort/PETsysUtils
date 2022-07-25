# created by Wilf Shorrock; June 2022
# python code to read output binary from petsys software and create useful plots
# of the data

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import argparse
import struct

# parse arguments
parser = argparse.ArgumentParser(\
    description='Read petsys binary file and make data plots')
parser.add_argument("-o",dest='fileName',type=str,required=True,\
    help='Prefix filename of binary file')
parser.add_argument("-m",dest='mappingFile',type=str,required=True,\
    help='Prefix filename of mapping file')
parser.add_argument('--channel',type=int,\
    help='Channel to plot the energy distribution of. \
        If not included all channels will be plotted')
parser.add_argument('--step1',type=float,help='Value of step1 to plot. \
        If not included all step1 values will be plotted')
parser.add_argument('--step2',type=float,help='Value of step2 to plot. \
        If not included all step2 values will be plotted')
parser.add_argument('--step1Title',type=str,default="Step1",\
    help='Title of step1 parameter')
parser.add_argument('--step2Title',type=str,default="Step2",\
    help='Title of step2 parameter')
args = parser.parse_args()

bfile = args.fileName+".ldat" # binary file containing data
sfile = args.fileName+".lidx" # text file containing step parameters
file = open(bfile,"rb")
byte = 1
time,en,chId = [],[],[]

# step through binary file and read information while storing in lists
while byte:
    byte = file.read(8) # read 8 bytes (32 bits)
    time.append(byte)
    byte = file.read(4) 
    en.append(byte)
    byte = file.read(4)
    chId.append(int.from_bytes(byte, byteorder='little'))
del byte

# convert binary to desired format
time = np.array(time)
time = time.view(dtype=np.int64)
en = np.array(en)
en = en.view(dtype=np.float32)
chId = np.array(chId)
data = pd.DataFrame({'time': time, 'energy': en, 'channelID': chId})
del time, en, chId

# read in parameter scan data from file
steps = pd.read_csv(sfile,header=None,sep='\s+',\
    names=['start event','end event','step1','step2'])

# read in channel mapping info
map = pd.read_csv(args.mappingFile+'.tsv', \
    sep='\t', header=None, \
    names = ['portID','slaveID','chipID','channelID','regionID',\
        'xi','yi','x','y','z'])

# calculate absolute channel IDs and add to mapping dataframe
map['absChID'] = map['chipID']*64 + map['channelID']

# format figure and plots
fig = plt.figure(figsize=(10,8))
nsteps1 = steps['step1'].nunique()
nsteps2 = steps['step2'].nunique()
if steps.shape[0] > 1:
    fig.suptitle("All steps")
if args.step1 != None:
    fig.suptitle(args.step1Title+": "+str(args.step1))
    if nsteps2 != 1 :
        if args.step2 != None:
            fig.suptitle(args.step1Title+": "+str(args.step1)+"; "+args.step2Title+": "+str(args.step2))
        else:
            fig.suptitle(args.step1Title+": "+str(args.step1)+"; "+args.step2Title+": All")
if args.step2 != None:
    fig.suptitle(""+args.step2Title+": "+str(args.step2))
    if nsteps1 != 1 :
        if args.step1 != None:
            fig.suptitle(args.step1Title+": "+str(args.step1)+"; "+args.step2Title+": "+str(args.step2))
        else:
            fig.suptitle(args.step1Title+": All; "+args.step2Title+": "+str(args.step2))
gs = gridspec.GridSpec(2,20)

heatMap = fig.add_subplot(gs[0,0:10])
heatMap.set_xlabel('x [pixels]')
heatMap.set_ylabel('y [pixels]')

chHist = fig.add_subplot(gs[0,12:])
chHist.set_xlabel('Channel ID')
chHist.set_ylabel('Entries')

enDist = fig.add_subplot(gs[1,:])
enDist.set_xlabel('Energy [ns]')
enDist.set_ylabel('Entries')

plt.subplots_adjust(top=0.92,right=0.95,left=0.1,bottom=0.1)

# retrieve the xi and yi values for the data entries using the mapping info
data['xi'] = data['channelID'].map(map.set_index('absChID')['xi'])
data['yi'] = data['channelID'].map(map.set_index('absChID')['yi'])

# start and end event for required step
startEvent = 0
endEvent = data.shape[0]
offset = 0.01
if args.step1 != None:
    startEvent = steps[(steps['step1']>args.step1-offset) &
        (steps['step1']<args.step1+offset)]['start event']
    endEvent = steps[(steps['step1']>args.step1-offset) &
        (steps['step1']<args.step1+offset)]['end event']
    if args.step2 != None:
        startEvent = steps[(steps['step1']>args.step1-offset) &
            (steps['step1']<args.step1+offset) &
            (steps['step2']>args.step2-offset) &
            (steps['step2']<args.step2+offset)]['start event']
        endEvent = steps[(steps['step1']>args.step1-offset) &
            (steps['step1']<args.step1+offset) &
            (steps['step2']>args.step2-offset) &
            (steps['step2']<args.step2+offset)]['end event']

if isinstance(startEvent, pd.Series):
    if startEvent.empty:
        print('ERROR: please give a correct step value')
        exit(1)
    else:
        startEvent = startEvent.at[0]
        endEvent = endEvent.at[0]

# plot and format the data
h = heatMap.hist2d(\
    data[startEvent:endEvent]['xi'],\
    data[startEvent:endEvent]['yi'],\
    bins=[8,8],range=[[0,8],[0,8]],cmin=1)
cbar = fig.colorbar(h[3], ax=heatMap)
cbar.formatter.set_powerlimits((0,4))
heatMap.grid(which='major',axis='both',linestyle='-',color='k',linewidth=2)

chHist.hist(\
    data[startEvent:endEvent]['channelID'],\
    bins=100,range=[300,400])
chHist.ticklabel_format(axis='y',style='sci',scilimits=(-3,4))

# extract energy data from specified channel if given
energy = data['energy']
enDist.set_title("All channels")
if args.channel:
    enDist.set_title("ch"+str(args.channel))
    energy = data[data[startEvent:endEvent]['channelID']==args.channel]['energy']

enDist.hist(energy,bins=5000,range=[-10,900])
enDist.set_xlim([-10,200])
enDist.ticklabel_format(axis='y',style='sci',scilimits=(-3,4))

plt.savefig(args.fileName+".pdf")
plt.show()
