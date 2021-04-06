'''
Example parser for RF logs.
'''

import os
import fnmatch
import os
import pandas as pd
from pycrate_asn1dir import J2735_NYC_03062020
from pycrate_asn1dir import ota_nyc
from pycrate_asn1rt.utils import *
import simplekml
from binascii import unhexlify
import hexdump
import easygui

InputLogDirectory = easygui.diropenbox(msg="Select Folder with Logs for Processing", title="Input for RF", default=None)
OutputLogDirectory = InputLogDirectory+'\\'
#InputLogDirectory = "C:\\GSAKTHI_Data\\Personal_Data\\PythonExamples\\NycLogs\\LogDecryption\\Input\\RF"
#OutputLogDirectory = "C:\\GSAKTHI_Data\\Personal_Data\\PythonExamples\\NycLogs\\Log_Output\\"

RFSummary = pd.DataFrame(columns=['Filename', 'SerialNo','Info'])

LogFilesList = os.listdir(InputLogDirectory)

def islogrf(input_log_file):
    #print("Function that finds out if Log is Bread Crumb Log")
    dummyrflog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDRF
    try:
        dummyrflog.from_uper(input_log_file)
    except:
        return 0
    else:
        return 1


def isrflogbsm(input_rf_file):
    #print("Function that finds out if the RF log for a BSM")
    try:
        get_val_at(input_rf_file, ['bsmRFList'])
    except:
        #print("Not bsmRFList")
        return 0
    else:
        #print("Data is bsmRFList")
        return 1

def isrflogmap(input_rf_file):
    #print("Function that finds out if the RF log for a MAP")
    try:
        get_val_at(input_rf_file, ['mapRFList'])
    except:
        #print("Not mapRFList")
        return 0
    else:
        #print("Data is mapRFList")
        return 1

def isrflogspat(input_rf_file):
    #print("Function that finds out if the RF log for a SPaT")
    try:
        get_val_at(input_rf_file, ['spatRFList'])
    except:
        #print("Not spatRFList")
        return 0
    else:
         #print("Data is spatRFList")
        return 1

def isrflogtim(input_rf_file):
    #print("Function that finds out if the RF log for a TIM")
    try:
        get_val_at(input_rf_file, ['timRFList'])
    except:
        #print("Not timRFList")
        return 0
    else:
        #print("Data is timRFList")
        return 1

def ProcessSpatInfo(input_rf_file):
#    print(get_val_at(dummyotalog['value']['status'][2]))
    dummy_data = get_val_at(input_rf_file,['spatRFList'])
    # print(dummy_data)
    # print(type(dummy_data))
    # print(dummy_data[0])
    return 0

def ProcessMapInfo(input_rf_file):
    return 1

def ProcessTimInfo(input_rf_file):
    return 1

def ProcessBsmInfo(input_rf_file):
    return 1

for i in range(len(LogFilesList)):
#    print("Processing File:" + LogFilesList[i])
    logfile = open(InputLogDirectory+'\\'+LogFilesList[i],"rb")
    contents =logfile.read()
    if islogrf(contents) == 1:
        RFLog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDRF
        RFLog.from_uper(contents)
        RFOutputFile = open(OutputLogDirectory + LogFilesList[i] + '.txt', "w")
        RFOutputFile.write(RFLog.to_asn1())
        RFOutputFile.close()
        serial_no = get_val_at(RFLog,['asdSerialNumber'])
        if isrflogbsm(RFLog) == 1:
            ProcessBsmInfo(RFLog)
            Type = "RF Log is a BSM RF Log"
        elif isrflogmap(RFLog) == 1:
            ProcessMapInfo(RFLog)
            Type = "RF Log is a MAP RF Log"
        elif isrflogspat(RFLog) == 1:
            ProcessSpatInfo(RFLog)
            Type = "RF Log is a SPaT RF Log"
        elif isrflogtim(RFLog) == 1:
            ProcessTimInfo(RFLog)
            Type = "RF Log is a TIM RF Log"
        else:
            Type = "RF Log is not valid type"
        RFSummary = RFSummary.append(
            {'Filename': LogFilesList[i], 'SerialNo' : serial_no, 'Info': Type}, ignore_index=True)
RFSummary.to_csv(OutputLogDirectory + "RFLog_ReportSummary" + '.csv', index=True, header=True)
print("Total no of RF files - Processed :", i+1)
print("Generated - RF Log Summary Report")
print("==============================================================================================")