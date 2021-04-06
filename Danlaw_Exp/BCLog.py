'''
Example parser for BC logs.
'''

import os
import fnmatch
import os
import pandas as pd
from pycrate_asn1dir import J2735_NYC_03062020
from pycrate_asn1dir import ota_nyc
from pycrate_asn1rt.utils import *
import simplekml
import datetime
from binascii import unhexlify
from math import sin, cos, sqrt, atan2, radians, floor, ceil
import hexdump
import easygui

InputLogDirectory = easygui.diropenbox(msg="Select Folder with Logs for Processing", title="Input for Bread Crumb", default=None)
OutputLogDirectory = InputLogDirectory+'\\'

#InputLogDirectory = "C:\\GSAKTHI_Data\\Personal_Data\\PythonExamples\\NycLogs\\LogDecryption\\Input\\BC"
#OutputLogDirectory = "C:\\GSAKTHI_Data\\Personal_Data\\PythonExamples\\NycLogs\\Log_Output\\"
BCSummary = pd.DataFrame(columns=['Filename', 'SerialNo'])

Loc_Factor = 10000000 # 10^-7 Degrees to Degrees
Spd_Factor = 0.02*2.23694 # 10^-2 mps to mph
Head_Factor = 0.0125
To_Radians = 0.01745329252
LogFilesList = os.listdir(InputLogDirectory)

def distancecalc(lat1,long1,lat2,long2):
    R = 6373.0
    lat1_rad = radians(lat1)
    long1_rad = radians(long1)
    lat2_rad = radians(lat2)
    long2_rad = radians(long2)
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c * 1000
    return distance

def bc2kml(input_bc_file,filename):
    #print("Function that converts NYC BreadCrumb Log to KML File")
    totaldistance = 0
    kml = simplekml.Kml()
#    print("SerialNumber of BC Log: " + get_val_at(input_bc_file, ['asdSerialNumber']))
#    print("Resolution of Bread Crumbs in BC Log: " + get_val_at(input_bc_file, ['timeRecordResolution']))
    bc = get_val_at(input_bc_file, ['locList'])
    numberofbc = len(bc)
    avgspeedlist = []
    #print(input_bc_file.to_asn1())
    for j in range(numberofbc):
        pnt = kml.newpoint(name="", coords=[(get_val_at(input_bc_file, ['locList', j, 'longitude'])/Loc_Factor, get_val_at(input_bc_file, ['locList', j, 'latitude'])/Loc_Factor)])
        pnt.iconstyle = simplekml.IconStyle(color = simplekml.Color.rgb(255, 0, 0), scale=0.5, heading=0, icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None, href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'), hotspot=None)
        #pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/info-i.png'
        #pnt.style.iconstyle.color = simplekml.Color.rgb(255, 0, 0)  # RGB values(255,255,0)
        if j > 0:
            tempdistance = distancecalc((get_val_at(input_bc_file, ['locList', j, 'latitude'])/Loc_Factor),(get_val_at(input_bc_file, ['locList', j, 'longitude'])/Loc_Factor),(get_val_at(input_bc_file, ['locList', j-1, 'latitude'])/10000000),(get_val_at(input_bc_file, ['locList', j-1, 'longitude'])/Loc_Factor))
            totaldistance = totaldistance + tempdistance
            temp1year = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'year'])
            temp1month = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'month'])
            temp1day = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'day'])
            temp1hour = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'hour'])
            temp1minute = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'minute'])
            temp1second = floor(get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'second']) / 1000)
            temp1microsec = (get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'second']) % 1000) * 1000
            temp1fulltime = datetime.datetime(temp1year, temp1month, temp1day, temp1hour, temp1minute, temp1second,temp1microsec)

            temp2year = get_val_at(input_bc_file, ['locList', j-1, 'timeStamp', 'year'])
            temp2month = get_val_at(input_bc_file, ['locList', j-1, 'timeStamp', 'month'])
            temp2day = get_val_at(input_bc_file, ['locList', j-1, 'timeStamp', 'day'])
            temp2hour = get_val_at(input_bc_file, ['locList', j-1, 'timeStamp', 'hour'])
            temp2minute = get_val_at(input_bc_file, ['locList', j-1, 'timeStamp', 'minute'])
            temp2second = floor(get_val_at(input_bc_file, ['locList', j-1, 'timeStamp', 'second']) / 1000)
            temp2microsec = (get_val_at(input_bc_file, ['locList', j-1, 'timeStamp', 'second']) % 1000) * 1000
            temp2fulltime = datetime.datetime(temp2year, temp2month, temp2day, temp2hour, temp2minute, temp2second,temp2microsec)

            temptraversersedtime = abs(temp1fulltime - temp2fulltime)
            if temptraversersedtime.total_seconds() != 0:
                tempavgspeed = round(tempdistance / temptraversersedtime.total_seconds(),5)
                avgspeedlist.append(tempavgspeed)
            else:
                print("Duplicate BC Log.. Avoid Divide by zero..")
        if j == 0:
            tempyear = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'year'])
            tempmonth = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'month'])
            tempday = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'day'])
            temphour = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'hour'])
            tempminute = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'minute'])
            tempsecond = floor(get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'second']) / 1000)
            tempmicrosec = (get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'second']) % 1000) * 1000
            firstbctime = datetime.datetime(tempyear, tempmonth, tempday, temphour, tempminute, tempsecond, tempmicrosec)
        if j == (numberofbc-1):
            tempyear = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'year'])
            tempmonth = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'month'])
            tempday = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'day'])
            temphour = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'hour'])
            tempminute = get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'minute'])
            tempsecond = floor(get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'second']) / 1000)
            tempmicrosec = (get_val_at(input_bc_file, ['locList', j, 'timeStamp', 'second']) % 1000) * 1000
            lastbctime = datetime.datetime(tempyear, tempmonth, tempday, temphour, tempminute, tempsecond, tempmicrosec)

    BCavgspeed = round(sum(avgspeedlist) / len(avgspeedlist),5)
    traversersedtime = abs(lastbctime - firstbctime)
    #print(traversersedtime.total_seconds())
    kml.save(OutputLogDirectory + '\\' + get_val_at(input_bc_file, ['asdSerialNumber']) + "_" + filename + '.kml')
    return

def islogbc(input_log_file):
    #print("Function that finds out if Log is Bread Crumb Log")
    dummybclog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDMobility
    try:
        dummybclog.from_uper(input_log_file)
    except:
        return 0
    else:
        return 1

for i in range(len(LogFilesList)):
#    print(i , "Processing File:" + LogFilesList[i])
    logfile = open(InputLogDirectory+'\\'+LogFilesList[i],"rb")
    contents =logfile.read()
    if islogbc(contents) == 1:
        BCLog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDMobility
        BCLog.from_uper(contents)
        BCOutputFile = open(OutputLogDirectory + LogFilesList[i] + '.txt', "w")
        BCOutputFile.write(BCLog.to_asn1())
        BCOutputFile.close()
        serial_no = get_val_at(BCLog,['asdSerialNumber'])
        bc2kml(BCLog,LogFilesList[i])
        BCSummary = BCSummary.append(
            {'Filename': LogFilesList[i], 'SerialNo' : serial_no}, ignore_index=True)
BCSummary.to_csv(OutputLogDirectory + "BCLog_ReportSummary" + '.csv', index=True, header=True)
print("Total no of BC files - Processed :", i+1)
print("Generated - BC Log Summary Report")
print("==============================================================================================")