# -*- coding: utf-8 -*-

# created by Wilf Shorrock, June 2022
# adds library of functions to save desired metadata to json file
# relies on the assumption that all channels are configured the same

from petsys import daqd, config
from copy import deepcopy
import os
import math
import time
import json


class meta:
    # finds the metadata in the given config file and saves as dictionary
    def findMeta(configFile):
        mask = config.LOAD_ALL
        systemConfig = config.ConfigFromFile(configFile, loadMask=mask)

        # save metadata to json file
        data = {
                 'time' : ,
                 'mode' : systemConfig.__asicChannelQDCModeTable,
                 'hwTrigger' : systemConfig.__hwTrigger,
                 'trigger_mode_1' : ,
                 'trigger_mode_2_t' : ,
                 'trigger_mode_2_1' : ,
                 'trigger_mode_2_e' : ,
                 'trigger_mode_2_b' : ,
                 'fe_delay' : asicsConfig[activeAsics[0]].channelConfig["fe_delay"]
               }
