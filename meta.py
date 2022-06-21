# -*- coding: utf-8 -*-

# created by Wilf Shorrock, June 2022
# adds library of functions to save desired metadata to json file
# relies on the assumption that all channels are configured the same

from petsys import config
import configparser
import time
import json


class Data:
    '''Holds the metadata for a single run'''
    def __init__(self):
        self.run = 0
        self.source = ''
        self.photosensors = ''
        self.start_time = None
        self.end_time = None
        self.run_time = 0
        self.mode = ''
        self.hwTrigger = ''
        self.trigger_mode_1 = 0
        self.trigger_mode_2_t = 0
        self.trigger_mode_2_q = 0
        self.trigger_mode_2_e = 0
        self.trigger_mode_2_b = 0
        self.fe_delay = 0
        self.start_temp = {}
        self.end_temp = {}
        self.BDV = 0
        self.OV = 0
        self.LSB_T1 = 0
        self.vth_t1 = 0
        self.vth_t2 = 0
        self.vth_e = 0
        self.scan_parameters = ''
        self.data = {}
    # finds the metadata in the given config file and saves as dictionary
    def findMeta(configFile):
        configParser = configparser.RawConfigParser()
        configParser.read(configFile)
        asicParams = config.parseAsicParameters(configParser)
        self.trigger_mode_1 = asicParams["channel","trigger_mode_1"]
        self.trigger_mode_2_t = asicParams["channel","trigger_mode_2_t"]
        self.trigger_mode_2_q = asicParams["channel","trigger_mode_2_q"]
        self.trigger_mode_2_e = asicParams["channel","trigger_mode_2_e"]
        self.trigger_mode_2_b = asicParams["channel","trigger_mode_2_b"]
        self.fe_delay = asicParams["channel","fe_delay"]
        self.LSB_T1 = asicParams["global","disc_lsb_t1"]

        # prepare data for json format
        self.data = {
                 'run' : self.run,
                 'source' : self.source,
                 'photosensors': self.photosensors,
                 'start time' : self.time,
                 'run time': self.run_time,
                 'mode' : self.mode,
                 'hwTrigger' : self.hwTrigger,
                 'trigger_mode_1' : self.trigger_mode_1,
                 'trigger_mode_2_t' : self.trigger_mode_2_t,
                 'trigger_mode_2_q' : self.trigger_mode_2_q,
                 'trigger_mode_2_e' : self.trigger_mode_2_e,
                 'trigger_mode_2_b' : self.trigger_mode_2_b,
                 'fe_delay' : self.fe_delay,
                 'start temp' : self.start_temp,
                 'end temp' : self.end_temp,
                 'BDV' : self.BDV,
                 'OV' : self.OV,
                 'LSB T1' : self.LSB_T1,
                 'vth_t1' : self.vth_t1,
                 'vth_t2' : self.vth_t2,
                 'vth_e' : self.vth_e,
                 'scan parameters' : self.scan_parameters
               }
    def saveMeta(filePrefix):
        file = filePrefix+".json"
        with open(file, 'w') as fp:
            json.dump(self.data, fp)
