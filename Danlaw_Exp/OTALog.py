'''
Example parser for Event logs.
'''


import os
from pycrate_asn1dir import J2735_NYC_03062020
from pycrate_asn1dir import ota_nyc
from pycrate_asn1rt.utils import *
import pandas as pd
import easygui
InputLogDirectory = easygui.diropenbox(msg="Select Folder with Logs for Processing", title="Input for OTA", default=None)
OutputLogDirectory = InputLogDirectory+'\\'
#InputLogDirectory = "C:\\GSAKTHI_Data\\Personal_Data\\PythonExamples\\NycLogs\\LogDecryption\\Input\\OTA"
#OutputLogDirectory = "C:\\GSAKTHI_Data\\Personal_Data\\PythonExamples\\NycLogs\\Log_Output\\"

LogFilesList = os.listdir(InputLogDirectory)
OtaSummary = pd.DataFrame(columns=['Filename', 'SerialNo', 'AppVersion', 'CfgVersion', 'FwVersion', 'KnlVersion', 'SecVersion'])

App_ver =  0
Cfg_ver = 0
Fw_ver = 0
Knl_ver = 0
Sec_ver = 0

def islogota(input_log_file):
    #print("Function that finds out if Log is OTA Log")
    dummyotalog = ota_nyc.OTA_NYC.NycOtaPdu
    try:
        dummyotalog.from_uper(input_log_file)
    except:
        return 0
    else:
        try:
            get_val_at(dummyotalog, ['value', 'OtaStatus'])
        except:
            return 0
        else:
            return 1

for i in range(len(LogFilesList)):
#    print(i , "Processing File:" + LogFilesList[i])
    logfile = open(InputLogDirectory+'\\'+LogFilesList[i],"rb")
    contents =logfile.read()
    if islogota(contents) == 1:
        OTALog = ota_nyc.OTA_NYC.NycOtaPdu
        OTALog.from_uper(contents)
        OTAOutputFile = open(OutputLogDirectory + '\\' + LogFilesList[i] + '.txt', "w")
        OTAOutputFile.write(OTALog.to_asn1())
        OTAOutputFile.close()

        list_len = len((get_val_at(OTALog, ['value', 'OtaStatus', 'status'])))
        Serial_no = (get_val_at(OTALog, ['value', 'OtaStatus', 'serial']))

        for j in range(list_len):
            file_id = get_val_at(OTALog, ['value', 'OtaStatus', 'status', j, 'fileId'])
            file_ver = get_val_at(OTALog, ['value', 'OtaStatus', 'status', j, 'fileRev'])
            if (file_id == 16720):
                App_ver = file_ver
            elif (file_id == 17222):
                Cfg_ver = file_ver
            elif (file_id == 18007):
                Fw_ver = file_ver
            elif (file_id == 19276):
                Knl_ver = file_ver
            elif (file_id == 19289):
                Sec_ver = file_ver
            else:
                App_ver = Cfg_ver = Fw_ver = Knl_ver = Sec_ver = 255
        OtaSummary = OtaSummary.append(
            {'Filename': LogFilesList[i], 'SerialNo': Serial_no, 'AppVersion': App_ver, 'CfgVersion': Cfg_ver,
             'FwVersion': Fw_ver, 'KnlVersion': Knl_ver, 'SecVersion': Sec_ver}, ignore_index=True)

OtaSummary.to_csv(InputLogDirectory+'\\' + "OtaSummary_ReportSummary" + '.csv', index=True, header=True)
print("Total no of OTA files - Processed :", i+1)
print("Generated - OTA Summary Report")
print("==============================================================================================")