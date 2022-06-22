# -*- coding: utf-8 -*-

# created by Wilf Shorrock, June 2022
# adds data class to find, store and save desired metadata 
# does not account for individually configured channels

from petsys import config
import configparser
import time
import json

class Data:
    def __init__(self):
        self.run = 0
        self.source = ''
        self.photosensors = ''
        self.material = ''
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
        self.step1par = ''
        self.step1 = []
        self.step2par = ''
        self.step2 = []
        self.status = 'NOT STARTED'
        self.data = {}
    def fillData(self):
        self.data = {
                 'run' : self.run,
                 'source' : self.source,
                 'photosensors': self.photosensors,
                 'material' : self.material,
                 'start time' : self.start_time,
                 'end time' : self.end_time,
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
                 'step1 parameter' : self.step1par,
                 'step1' : self.step1,
                 'step2 parameter' : self.step2par,
                 'step2' : self.step2,
                 'status' : self.status
               }
    # finds the metadata in the given config file and saves as dictionary
    def findMeta(self, configFile):
        configParser = configparser.RawConfigParser()
        configParser.read(configFile)
        if not configParser.has_section("other"):
            print("ERROR: please add 'other' section to config file")
            exit(1)
        for key, value in configParser.items("other"):
            if key not in ["photosensors","source","material"]:
                print("Invalid other parameter: '%s'" % key)
                exit(1)
        self.source = configParser.get("other","source")
        self.photosensors = configParser.get("other","photosensors")
        self.material = configParser.get("other","material")
        self.trigger_mode_1 = configParser.get("asic_parameters","channel.trigger_mode_1", fallback='DEFAULT')
        self.trigger_mode_2_t = configParser.get("asic_parameters","channel.trigger_mode_2_t", fallback='DEFAULT')
        self.trigger_mode_2_q = configParser.get("asic_parameters","channel.trigger_mode_2_q", fallback='DEFAULT')
        self.trigger_mode_2_e = configParser.get("asic_parameters","channel.trigger_mode_2_e", fallback='DEFAULT')
        self.trigger_mode_2_b = configParser.get("asic_parameters","channel.trigger_mode_2_b", fallback='DEFAULT')
        self.fe_delay = configParser.get("asic_parameters","channel.fe_delay", fallback='DEFAULT')
        self.LSB_T1 = configParser.get("asic_parameters","global.disc_lsb_t1", fallback='DEFAULT')
        self.status = 'INCOMPLETE'

        # prepare data for json format
        self.fillData()
        
    def saveMeta(self, filePrefix):
        file = filePrefix+".json"
        self.fillData()
        with open(file, 'w') as fp:
            json.dump(self.data, fp, indent=4)
