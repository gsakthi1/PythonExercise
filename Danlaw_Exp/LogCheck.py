'''
Goal :
1) Get the folder location from user
2) Check the folder for valid files
3) Print the total no of log files
4) Print the no of files each log category
'''

import os
import easygui
import glob
import shutil
from shutil import copyfile

NoOfFiles = 0
Ssl_NoOfFiles = 0
Bc_NoOfFiles = 0
Ota_NoOfFiles = 0
Rf_NoOfFiles = 0
Evt_NoOfFiles = 0

InputLogDirectory = easygui.diropenbox(msg="Select Folder with Logs for Processing", title="Input for All Logs", default=None)
#InputLogDirectory = "C:\\GSAKTHI_Data\\Personal_Data\\PythonExamples\\NycLogs\\Log_Input"
#InputLogDirectory = "C:\\GSAKTHI_Data\\Personal_Data\\PythonExamples\\NycLogs\\LogDecryption\\Input"
ssl_path = InputLogDirectory + '\\' + 'SSL'
rf_path = InputLogDirectory + '\\' + 'RF'
evt_path = InputLogDirectory + '\\' + 'EVT'
bc_path = InputLogDirectory + '\\' + 'BC'
ota_path = InputLogDirectory + '\\' + 'OTA'

dirListing = os.listdir(ssl_path)
Ssl_NoOfFiles = (len(dirListing))

dirListing = os.listdir(rf_path)
Rf_NoOfFiles = (len(dirListing))

dirListing = os.listdir(ota_path)
Ota_NoOfFiles = (len(dirListing))

dirListing = os.listdir(evt_path)
Evt_NoOfFiles = (len(dirListing))

dirListing = os.listdir(bc_path)
Bc_NoOfFiles = (len(dirListing))

# for (path, dirs, files) in os.walk(InputLogDirectory):
#   for file in files:
#     filename = os.path.join(path, file)
#     if file.startswith('RF_'):
#        Rf_NoOfFiles += 1
#  #      shutil.move(os.path.join(path, file), os.path.join(rf_path, filename))
#     if file.startswith('EV'):
#        Evt_NoOfFiles += 1
#  #      shutil.move(os.path.join(path, file), os.path.join(evt_path, filename))
#     if file.startswith('OTA'):
#        Ota_NoOfFiles += 1
#  #      shutil.move(os.path.join(path, file), os.path.join(ota_path, filename))
#     if file.startswith('BC'):
#        Bc_NoOfFiles += 1
#  #      shutil.move(os.path.join(path, file), os.path.join(bc_path, filename))
#     if file.startswith('SSL'):
#        Ssl_NoOfFiles += 1
#  #      shutil.move(os.path.join(path, file), ssl_path)

print("Total No Of Log files : ", Rf_NoOfFiles+Evt_NoOfFiles+Ota_NoOfFiles+Bc_NoOfFiles+Ssl_NoOfFiles)
print("Total No Of RF Log files : ",Rf_NoOfFiles)
print("Total No Of OTA Log files : ",Ota_NoOfFiles)
print("Total No Of Event Log files : ",Evt_NoOfFiles)
print("Total No Of Bread Crumb Log files : ",Bc_NoOfFiles)
print("Total No Of SSL Log files : ",Ssl_NoOfFiles)
print("==============================================================================================")