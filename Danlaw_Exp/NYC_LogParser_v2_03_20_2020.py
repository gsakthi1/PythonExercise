'''
NYC Log parser for NYC ASD Based logs.
Version : 1
Date : 03/13/2020

Version : 2
Date : 03/13/2020
NYC Log parser for NYC ASD Based logs.
CSV report generated with BSM, TIM, MAP, SPAT list availability

Version : 3
Date : 03/18/2020
NYC Log parser for NYC ASD Based logs.
Added capability to read Logs in JSON Format

Version : 4
Date : 03/20/2020
NYC Log parser for NYC ASD Based logs.
Added capability to process MAP, SPaT and TIM RF Logs
'''

current_version = 4

import os
import fnmatch
import os
from pycrate_asn1dir import J2735_NYC_03062020
from pycrate_asn1dir import ota_nyc
from pycrate_asn1rt.utils import *
import pandas as pd
import matplotlib.pyplot as plt
import simplekml
from math import sin, cos, sqrt, atan2, radians, floor, ceil
import datetime
from fpdf import FPDF
from binascii import unhexlify
import hexdump
import easygui
import getpass

username = getpass.getuser()
print(username)
default_browser_path = "C:\\Users\\" + str(username) + "\\Desktop\\"
print(default_browser_path)

# InputLogDirectory = "C:\\Users\\rojerb\\PycharmProjects\\NYCLogsDecoder\\EncodedLogs"
# OutputLogDirectory = "C:\\Users\\rojerb\\PycharmProjects\\NYCLogsDecoder\\DecodedLogs"
# MAP_SPaT_DB_FilePath = "C:\\VBoxShare\\NYC_Logs_Decoder_Database\\RSU_MAPSPaT_Table.csv"
# TIM_DB_FilePath = "C:\\VBoxShare\\NYC_Logs_Decoder_Database\\RSU_TIM_Table.csv"

InputLogDirectory = easygui.diropenbox(msg="Select Folder with Logs for Processing", title="NYC_LogParser_v" + str(current_version), default=default_browser_path)
OutputLogDirectory = easygui.diropenbox(msg="Select Folder to save Output", title="NYC_LogParser_v" + str(current_version), default=default_browser_path)
MAP_SPaT_DB_FilePath = easygui.fileopenbox(msg="Select MAP_SPaT CSV Database File", title="NYC_LogParser_v" + str(current_version), default=default_browser_path)
TIM_DB_FilePath = easygui.fileopenbox(msg="Select TIM CSV Database File", title="NYC_LogParser_v" + str(current_version), default=default_browser_path)

MAP_SPaT_DB = pd.read_csv(MAP_SPaT_DB_FilePath, dtype=str)
print(MAP_SPaT_DB)
MAP_SPaT_DB_Cleaned = MAP_SPaT_DB[MAP_SPaT_DB.AstcId.ne("0") & MAP_SPaT_DB.AstcId.notnull() & MAP_SPaT_DB.RsuLocLatitude.ne("0") & MAP_SPaT_DB.RsuLocLatitude.notnull() & MAP_SPaT_DB.RsuLocLongitude.ne("0") & MAP_SPaT_DB.RsuLocLongitude.notnull() & MAP_SPaT_DB.RsuId.ne("0") & MAP_SPaT_DB.RsuId.notnull()]
print(MAP_SPaT_DB_Cleaned)

TIM_DB = pd.read_csv(TIM_DB_FilePath, dtype=str)
print(TIM_DB)
TIM_DB_Cleaned = TIM_DB[TIM_DB.PacketId.ne("0") & TIM_DB.PacketId.notnull() & TIM_DB.RsuId.ne("0") & TIM_DB.RsuId.notnull()]
print(TIM_DB_Cleaned)

# List of unique V2I Messages from RF Logs
MAP_Unique_list = []
TIM_Unique_list = []
SPaT_Unique_list = []
Evt_Lat =[]
Evt_Long = []
Evt_Speed = []
Evt_Sequence = []
TIMPresence = 0
MAPPresence = 0
SPATPresence = 0
BSMPresence = 0
HTrigger = 0
Loc_Factor = 10000000 # 10^-7 Degrees to Degrees
Spd_Factor = 0.02*2.23694 # 10^-2 mps to mph
Head_Factor = 0.0125
To_Radians = 0.01745329252

LogFilesList = os.listdir(InputLogDirectory)
EvtSummary = pd.DataFrame(
    columns=['Filename', 'BSM_Count', 'BSMList', 'TIMList', 'MAPList', 'SPATList', 'TriggerSequence'])

def CheckMsgPresence(input_evt_file):
    global TIMPresence, BSMPresence, MAPPresence, SPATPresence
    with open(input_evt_file) as f:
        if 'bsmList' in f.read():
            BSMPresence = True
    with open(input_evt_file) as f:
        if 'timList' in f.read():
            TIMPresence = True
    with open(input_evt_file) as f:
        if 'mapList' in f.read():
            MAPPresence = True
    with open(input_evt_file) as f:
        if 'spatList' in f.read():
            SPATPresence = True
    return 0

def ResetVariables():
    global TIMPresence, BSMPresence, MAPPresence, SPATPresence
    TIMPresence = False
    MAPPresence = False
    SPATPresence = False
    BSMPresence = False
    return 0

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

def islogbc(input_log_file):
    #print("Function that finds out if Log is Bread Crumb Log")
    dummybclog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDMobility
    try:
        dummybclog.from_uper(input_log_file)
    except:
        return 0
    else:
        return 1

def islogbc_json(input_log_file):
    #print("Function that finds out if Log is Bread Crumb Log in JSON Format")
    dummybclog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDMobility
    try:
        dummybclog.from_json(input_log_file)
    except:
        return 0
    else:
        return 1

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

def islogota_json(input_log_file):
    #print("Function that finds out if Log is OTA Log")
    dummyotalog = ota_nyc.OTA_NYC.NycOtaPdu
    try:
        dummyotalog.from_json(input_log_file)
    except:
        return 0
    else:
        try:
            get_val_at(dummyotalog, ['value', 'OtaStatus'])
        except:
            return 0
        else:
            return 1

def islogrf(input_log_file):
    #print("Function that finds out if Log is Bread Crumb Log")
    dummyrflog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDRF
    try:
        dummyrflog.from_uper(input_log_file)
    except:
        return 0
    else:
        return 1

def islogrf_json(input_log_file):
    #print("Function that finds out if Log is Bread Crumb Log")
    dummyrflog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDRF
    try:
        dummyrflog.from_json(input_log_file)
    except:
        return 0
    else:
        return 1

def islogevent(input_log_file):
    #print("Function that finds out if Log is Bread Crumb Log")
    dummyeventlog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdEvent
    try:
        dummyeventlog.from_uper(input_log_file)
    except:
        return 0
    else:
        return 1

def islogevent_json(input_log_file):
    #print("Function that finds out if Log is Bread Crumb Log")
    dummyeventlog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdEvent
    try:
        dummyeventlog.from_json(input_log_file)
    except:
        return 0
    else:
        return 1

def bc2kml(input_bc_file,filename):
    #print("Function that converts NYC BreadCrumb Log to KML File")
    totaldistance = 0
    kml = simplekml.Kml()
    print("SerialNumber of BC Log: " + get_val_at(input_bc_file, ['asdSerialNumber']))
    print("Resolution of Bread Crumbs in BC Log: " + get_val_at(input_bc_file, ['timeRecordResolution']))
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
    print("TimeStamp of First BC Entry= " + str(firstbctime))
    print("TimeStamp of Last BC Entry= " + str(lastbctime))
    print("Total time between first and last BC= " + str(traversersedtime.total_seconds()) + "seconds")
    print("Total Distance travelled in BC Log (m): " + str(round(totaldistance,2)) + " m")
    print("Total Distance travelled in BC Log (km): " + str(round(totaldistance / 1000,2)) + " km" )
    print("Average Speed in BC Log (mps): " + str(BCavgspeed) + " mps")
    print("Average Speed in BC Log (mph): " + str(round(BCavgspeed * 2.23694,2)) + " mph")

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Processed File Name" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + filename, ln=1, align="L")
    pdf.cell(200, 10, txt="Processed File Type" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + "Bread Crumb Log", ln=1, align="L")
    pdf.cell(200, 10, txt="Processed File ASN Version" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + "J2735_NYC_03062020", ln=1, align="L")
    pdf.cell(200, 10, txt="Serial Number of ASD" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + get_val_at(input_bc_file, ['asdSerialNumber']), ln=1, align="L")
    pdf.cell(200, 10, txt="Resolution of Bread Crumbs" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + get_val_at(input_bc_file, ['timeRecordResolution']), ln=1, align="L")
    pdf.cell(200, 10, txt="TimeStamp of First BC Entry" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + str(firstbctime), ln=1, align="L")
    pdf.cell(200, 10, txt="TimeStamp of Last BC Entry" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + str(lastbctime), ln=1, align="L")
    pdf.cell(200, 10, txt="Total time between first and last BC" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + str(traversersedtime.total_seconds()) + "seconds", ln=1, align="L")
    pdf.cell(200, 10, txt="Total Distance travelled in BC Log (m)" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + str(round(totaldistance,2)) + " m", ln=1, align="L")
    pdf.cell(200, 10, txt="Total Distance travelled in BC Log (km)" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + str(round(totaldistance / 1000,2)) + " km", ln=1, align="L")
    pdf.cell(200, 10, txt="Average Speed in BC Log (mps)" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + str(BCavgspeed) + " mps", ln=1, align="L")
    pdf.cell(200, 10, txt="Average Speed in BC Log (mph)" + "\t" + "\t" + "\t" + "\t" + "\t" + ":" + "\t" + str(round(BCavgspeed * 2.23694,2)) + " mph", ln=1, align="L")
    pdf.output(OutputLogDirectory + '\\' + get_val_at(input_bc_file, ['asdSerialNumber']) + "_" + filename + '.pdf')

    #print(totaldistance)

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

def process_map_rf(input_rf_log, filename):
    #print(input_rf_log.to_asn1())
    #print(get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPTime']))
    temp1year = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPTime', 'year'])
    temp1month = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPTime', 'month'])
    temp1day = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPTime', 'day'])
    temp1hour = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPTime', 'hour'])
    temp1minute = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPTime', 'minute'])
    temp1second = floor(get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPTime', 'second']) / 1000)
    temp1microsec = (get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPTime', 'second']) % 1000) * 1000
    temp1fulltime = datetime.datetime(temp1year, temp1month, temp1day, temp1hour, temp1minute, temp1second,
                                      temp1microsec)
    print(get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPRecord', 'msgHeader', 'myRFLevel']))
    firstmap_id = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPRecord', 'mapMsg', 'intersections', 0, 'id', 'id'])
    first_sight_lat = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPLocation', 'coreData', 'lat']) / Loc_Factor
    first_sight_long = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPLocation', 'coreData', 'long']) / Loc_Factor
    first_sight_speed = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPLocation', 'coreData', 'speed'])
    first_sight_head = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPLocation', 'coreData', 'heading']) * Head_Factor

    #print(get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPTime']))
    temp2year = get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPTime', 'year'])
    temp2month = get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPTime', 'month'])
    temp2day = get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPTime', 'day'])
    temp2hour = get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPTime', 'hour'])
    temp2minute = get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPTime', 'minute'])
    temp2second = floor(get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPTime', 'second']) / 1000)
    temp2microsec = (get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPTime', 'second']) % 1000) * 1000
    temp2fulltime = datetime.datetime(temp2year, temp2month, temp2day, temp2hour, temp2minute, temp2second,
                                      temp2microsec)
    print(get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPRecord', 'msgHeader', 'myRFLevel']))
    lastmap_id = get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPRecord', 'mapMsg', 'intersections', 0, 'id', 'id'])
    last_sight_lat = get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPLocation', 'coreData', 'lat']) / Loc_Factor
    last_sight_long = get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPLocation', 'coreData', 'long']) / Loc_Factor
    last_sight_speed = get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPLocation', 'coreData', 'speed'])
    last_sight_head = get_val_at(input_rf_log, ['mapRFList', 0, 'lastMAPLocation', 'coreData', 'heading']) * Head_Factor


    map_refP_lat = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPRecord', 'mapMsg', 'intersections', 0, 'refPoint', 'lat']) / Loc_Factor
    map_refP_long = get_val_at(input_rf_log, ['mapRFList', 0, 'firstMAPRecord', 'mapMsg', 'intersections', 0, 'refPoint',
                                             'long']) / Loc_Factor

    traversersedtime = abs(temp1fulltime - temp2fulltime)

    if firstmap_id == lastmap_id:
        if traversersedtime.total_seconds != 0:
            print("Valid MAP RF Log")

            MAP_RSU_Pos = MAP_SPaT_DB_Cleaned[MAP_SPaT_DB_Cleaned.AstcId.eq(str(firstmap_id))]
            #print(MAP_RSU_Pos)
            if MAP_RSU_Pos.empty:
                print("No matching Intersection ID found in database.. Skipping..")
            else:
                MAP_RSUL_lat = int(MAP_RSU_Pos.iloc[0].RsuLocLatitude) / Loc_Factor
                MAP_RSUL_long = int(MAP_RSU_Pos.iloc[0].RsuLocLongitude) / Loc_Factor

                kml = simplekml.Kml()
                pnt = kml.newpoint(name="", coords=[(MAP_RSUL_long, MAP_RSUL_lat)])
                pnt.iconstyle = simplekml.IconStyle(scale=2, heading=0,
                                                icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None,
                                                                    href='http://maps.google.com/mapfiles/kml/paddle/M.png'),
                                                hotspot=None)
                pnt = kml.newpoint(name="", coords=[(first_sight_long, first_sight_lat)])
                pnt.iconstyle = simplekml.IconStyle(color=simplekml.Color.rgb(0, 255, 0), scale=0.4, heading=first_sight_head - 180,
                                                icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None,
                                                                    href='http://maps.google.com/mapfiles/kml/shapes/arrow.png'),
                                                hotspot=None)
                pnt = kml.newpoint(name="", coords=[(last_sight_long, last_sight_lat)])
                pnt.iconstyle = simplekml.IconStyle(color=simplekml.Color.rgb(0, 0, 255), scale=0.4, heading=last_sight_head - 180,
                                                icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None,
                                                                    href='http://maps.google.com/mapfiles/kml/shapes/arrow.png'),
                                                hotspot=None)
                kml.save(
                    OutputLogDirectory + '\\' + str(firstmap_id) + "_MAP_" + get_val_at(input_rf_log, ['asdSerialNumber']) + "_" + filename + '.kml')
                print("MAPRF -> BSM Heading in RF Log (Last):" + str(first_sight_head))
                print("MAPRF ->BSM Heading in RF Log (Last):" + str(last_sight_head))
                print("MAPRF ->BSM Speed in RF Log (Last):" + str(first_sight_speed))
                print("MAPRF ->BSM Speed in RF Log (Last):" + str(last_sight_speed))
        else:
            print("Invalid MAP RF Log. MAP RF Log Time Difference is 0.")
    else:
        print("Invalid MAP RF Log. First and Last MAP Entries have different MAP Messages")

def process_spat_rf(input_rf_log, filename):
    #print(input_rf_log.to_asn1())
    #print(get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTTime']))
    temp1year = get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTTime', 'year'])
    temp1month = get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTTime', 'month'])
    temp1day = get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTTime', 'day'])
    temp1hour = get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTTime', 'hour'])
    temp1minute = get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTTime', 'minute'])
    temp1second = floor(get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTTime', 'second']) / 1000)
    temp1microsec = (get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTTime', 'second']) % 1000) * 1000
    temp1fulltime = datetime.datetime(temp1year, temp1month, temp1day, temp1hour, temp1minute, temp1second,
                                      temp1microsec)
    print(get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTRecord', 'msgHeader', 'myRFLevel']))
    firstmap_id = get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTRecord', 'spatMsg', 'intersections', 0, 'id', 'id'])
    first_sight_lat = get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTLocation', 'coreData', 'lat']) / Loc_Factor
    first_sight_long = get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTLocation', 'coreData', 'long']) / Loc_Factor
    first_sight_speed = get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTLocation', 'coreData', 'speed'])
    first_sight_head = get_val_at(input_rf_log, ['spatRFList', 0, 'firstSPaTLocation', 'coreData', 'heading']) * Head_Factor

    #print(get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTTime']))
    temp2year = get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTTime', 'year'])
    temp2month = get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTTime', 'month'])
    temp2day = get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTTime', 'day'])
    temp2hour = get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTTime', 'hour'])
    temp2minute = get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTTime', 'minute'])
    temp2second = floor(get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTTime', 'second']) / 1000)
    temp2microsec = (get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTTime', 'second']) % 1000) * 1000
    temp2fulltime = datetime.datetime(temp2year, temp2month, temp2day, temp2hour, temp2minute, temp2second,
                                      temp2microsec)
    print(get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTRecord', 'msgHeader', 'myRFLevel']))
    lastmap_id = get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTRecord', 'spatMsg', 'intersections', 0, 'id', 'id'])
    last_sight_lat = get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTLocation', 'coreData', 'lat']) / Loc_Factor
    last_sight_long = get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTLocation', 'coreData', 'long']) / Loc_Factor
    last_sight_speed = get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTLocation', 'coreData', 'speed'])
    last_sight_head = get_val_at(input_rf_log, ['spatRFList', 0, 'lastSPaTLocation', 'coreData', 'heading']) * Head_Factor

    traversersedtime = abs(temp1fulltime - temp2fulltime)

    if firstmap_id == lastmap_id:
        if traversersedtime.total_seconds != 0:
            print("Valid SPaT RF Log")

            SPaT_RSU_Pos = MAP_SPaT_DB_Cleaned[MAP_SPaT_DB_Cleaned.AstcId.eq(str(firstmap_id))]
            #print(SPaT_RSU_Pos)
            if SPaT_RSU_Pos.empty:
                print("No matching Intersection ID found in database.. Skipping..")
            else:
                SPaT_RSUL_lat = int(SPaT_RSU_Pos.iloc[0].RsuLocLatitude) / Loc_Factor
                SPaT_RSUL_long = int(SPaT_RSU_Pos.iloc[0].RsuLocLongitude) / Loc_Factor

                kml = simplekml.Kml()
                pnt = kml.newpoint(name="", coords=[(SPaT_RSUL_long, SPaT_RSUL_lat)])
                pnt.iconstyle = simplekml.IconStyle(scale=2, heading=0,
                                                icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None,
                                                                    href='http://maps.google.com/mapfiles/kml/paddle/S.png'),
                                                hotspot=None)
                pnt = kml.newpoint(name="", coords=[(first_sight_long, first_sight_lat)])
                pnt.iconstyle = simplekml.IconStyle(color=simplekml.Color.rgb(0, 255, 0), scale=0.4, heading=first_sight_head - 180,
                                                icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None,
                                                                    href='http://maps.google.com/mapfiles/kml/shapes/arrow.png'),
                                                hotspot=None)
                pnt = kml.newpoint(name="", coords=[(last_sight_long, last_sight_lat)])
                pnt.iconstyle = simplekml.IconStyle(color=simplekml.Color.rgb(0, 0, 255), scale=0.4, heading=last_sight_head - 180,
                                                icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None,
                                                                    href='http://maps.google.com/mapfiles/kml/shapes/arrow.png'),
                                                hotspot=None)
                kml.save(
                    OutputLogDirectory + '\\' + str(firstmap_id) + "_SPaT_" + get_val_at(input_rf_log, ['asdSerialNumber']) + "_" + filename + '.kml')
                print("SPaTRF -> BSM Heading in RF Log (Last):" + str(first_sight_head))
                print("SPaTRF ->BSM Heading in RF Log (Last):" + str(last_sight_head))
                print("SPaTRF ->BSM Speed in RF Log (Last):" + str(first_sight_speed))
                print("SPaTRF ->BSM Speed in RF Log (Last):" + str(last_sight_speed))
        else:
            print("Invalid SPaT RF Log. SPaT RF Log Time Difference is 0.")
    else:
        print("Invalid SPaT RF Log. First and Last SPaT Entries have different SPaT Messages")

def process_tim_rf(input_rf_log, filename):
    temp1year = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMTime', 'year'])
    temp1month = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMTime', 'month'])
    temp1day = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMTime', 'day'])
    temp1hour = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMTime', 'hour'])
    temp1minute = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMTime', 'minute'])
    temp1second = floor(get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMTime', 'second']) / 1000)
    temp1microsec = (get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMTime', 'second']) % 1000) * 1000
    temp1fulltime = datetime.datetime(temp1year, temp1month, temp1day, temp1hour, temp1minute, temp1second,
                                      temp1microsec)
    print(get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMRecord', 'msgHeader', 'myRFLevel']))
    firsttim_id = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMRecord', 'timMsg', 'packetID'])
    first_sight_lat = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMLocation', 'coreData', 'lat']) / Loc_Factor
    first_sight_long = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMLocation', 'coreData', 'long']) / Loc_Factor
    first_sight_speed = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMLocation', 'coreData', 'speed'])
    first_sight_head = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMLocation', 'coreData', 'heading']) * Head_Factor

    #print(get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMTime']))
    temp2year = get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMTime', 'year'])
    temp2month = get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMTime', 'month'])
    temp2day = get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMTime', 'day'])
    temp2hour = get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMTime', 'hour'])
    temp2minute = get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMTime', 'minute'])
    temp2second = floor(get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMTime', 'second']) / 1000)
    temp2microsec = (get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMTime', 'second']) % 1000) * 1000
    temp2fulltime = datetime.datetime(temp2year, temp2month, temp2day, temp2hour, temp2minute, temp2second,
                                      temp2microsec)
    print(get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMRecord', 'msgHeader', 'myRFLevel']))
    lasttim_id = get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMRecord', 'timMsg', 'packetID'])
    last_sight_lat = get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMLocation', 'coreData', 'lat']) / Loc_Factor
    last_sight_long = get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMLocation', 'coreData', 'long']) / Loc_Factor
    last_sight_speed = get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMLocation', 'coreData', 'speed'])
    last_sight_head = get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMLocation', 'coreData', 'heading']) * Head_Factor


    tim_refP_lat = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMRecord', 'timMsg', 'dataFrames', 0, 'msgId', 'roadSignID', 'position', 'lat']) / Loc_Factor
    tim_refP_long = get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMRecord', 'timMsg', 'dataFrames', 0, 'msgId',
                                             'roadSignID', 'position', 'long']) / Loc_Factor

    traversersedtime = abs(temp1fulltime - temp2fulltime)

    # TODO - PacketID Read is reading 0x4E as "N" Need to Fix
    # print(input_rf_log.to_asn1())
    # print("Rojer" + str(firsttim_id))
    # print(get_val_at(input_rf_log, ['timRFList', 0, 'firstTIMRecord', 'timMsg', 'packetID']))
    # print(lasttim_id)
    # print(get_val_at(input_rf_log, ['timRFList', 0, 'lastTIMRecord', 'timMsg', 'packetID']))

    if firsttim_id == lasttim_id:
        if traversersedtime.total_seconds != 0:
            print("Valid TIM RF Log")
            # firstmap_id + filename
            # http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png
            kml = simplekml.Kml()
            pnt = kml.newpoint(name="", coords=[(tim_refP_long, tim_refP_lat)])
            pnt.iconstyle = simplekml.IconStyle(scale=2, heading=0,
                                                icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None,
                                                                    href='http://maps.google.com/mapfiles/kml/paddle/T.png'),
                                                hotspot=None)
            pnt = kml.newpoint(name="", coords=[(first_sight_long, first_sight_lat)])
            pnt.iconstyle = simplekml.IconStyle(color=simplekml.Color.rgb(0, 255, 0), scale=0.4, heading=first_sight_head - 180,
                                                icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None,
                                                                    href='http://maps.google.com/mapfiles/kml/shapes/arrow.png'),
                                                hotspot=None)
            pnt = kml.newpoint(name="", coords=[(last_sight_long, last_sight_lat)])
            pnt.iconstyle = simplekml.IconStyle(color=simplekml.Color.rgb(0, 0, 255), scale=0.4, heading=last_sight_head - 180,
                                                icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None,
                                                                    href='http://maps.google.com/mapfiles/kml/shapes/arrow.png'),
                                                hotspot=None)
            temp_str = str(firsttim_id)
            temp_str = temp_str.replace("\\x", "")
            temp_str = temp_str.replace("b'", "")
            temp_str = temp_str.replace("'", "")
            print(str(firsttim_id))
            print(temp_str)
            kml.save(
                OutputLogDirectory + '\\' + temp_str[0:2] + "_" + temp_str[-4:] + "_TIM_" + get_val_at(input_rf_log, ['asdSerialNumber']) + "_" + filename + '.kml')
            print("TIMRF -> BSM Heading in RF Log (Last):" + str(first_sight_head))
            print("TIMRF ->BSM Heading in RF Log (Last):" + str(last_sight_head))
            print("TIMRF ->BSM Speed in RF Log (Last):" + str(first_sight_speed))
            print("TIMRF ->BSM Speed in RF Log (Last):" + str(last_sight_speed))

        else:
            print("Invalid TIM RF Log. TIM RF Log Time Difference is 0.")
    else:
        print("Invalid TIM RF Log. First and Last TIM Entries have different TIM Messages")


def find_rflog_type_and_process(input_rf_log, filename):
    #print("Function that finds out if the RF log for a TIM")
    if isrflogbsm(input_rf_log) == 1:
        print("RF Log is a BSM RF Log")
    elif isrflogmap(input_rf_log) == 1:
        print("RF Log is a MAP RF Log")
        process_map_rf(input_rf_log, filename)
    elif isrflogspat(input_rf_log) == 1:
        print("RF Log is a SPaT RF Log")
        process_spat_rf(input_rf_log, filename)
    elif isrflogtim(input_rf_log) == 1:
        print("RF Log is a TIM RF Log")
        process_tim_rf(input_rf_log, filename)
    else:
        print("RF Log is not valid type")

def ProcessEventInfo(input_evt_file):
    dummy_data = get_val_at(input_evt_file, ['eventHeader'])
    dummy_evt_type = get_val_at(input_evt_file, ['eventHeader','eventType'])
#    print(type(dummy_data))
#    print("Event Type - ", dummy_evt_type)
    return dummy_evt_type

def GetEvent_HostTrigger(input_evt_file):
    dummy_evt_type = get_val_at(input_evt_file, ['eventHeader','eventType'])
    dummy_evt_hostTrigger = 0
    dummy_evt_hostTrigger = get_val_at(input_evt_file, ['eventHeader', 'triggerHVSeqNum'])
    return dummy_evt_hostTrigger

def GetEvent_HostTLatitude(input_evt_file):
    dummy_latitude = []
    dummy_data = get_val_at(input_evt_file, ['bsmList'])
#    print(type(dummy_data), len(dummy_data))
    for i in range(len(dummy_data)):
        dummy_latitude.append(dummy_data[i]['bsmRecord']['bsmMsg']['coreData']['lat'])
    return dummy_latitude

def GetEvent_HostLongitude(input_evt_file):
    dummy_longitude = []
    dummy_data = get_val_at(input_evt_file, ['bsmList'])
#    print(type(dummy_data), len(dummy_data))
    for i in range(len(dummy_data)):
        dummy_longitude.append(dummy_data[i]['bsmRecord']['bsmMsg']['coreData']['long'])
    return dummy_longitude

def GetEvent_HostSpeed(input_evt_file):
    dummy_speed = []
    dummy_data = get_val_at(input_evt_file, ['bsmList'])
#    print(type(dummy_data), len(dummy_data))
    for i in range(len(dummy_data)):
        dummy_speed.append(dummy_data[i]['bsmRecord']['bsmMsg']['coreData']['speed'])
    return dummy_speed

def GetEvent_SeqNo(input_evt_file):
    dummy_seq = []
    dummy_data = get_val_at(input_evt_file, ['bsmList'])
    for i in range(len(dummy_data)):
        dummy_seq.append(dummy_data[i]['eventMsgSeqNum'])
    return dummy_seq

for i in range(len(LogFilesList)):
    print(i , "Processing File:" + LogFilesList[i])
    logfile = open(InputLogDirectory+'\\'+LogFilesList[i],"rb")
    contents =logfile.read()
    if islogevent(contents) == 1:
        EventLog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdEvent
        EventLog.from_uper(contents)
        #Check the type of Event log
        EV_type = (ProcessEventInfo(EventLog)).upper()
        EvtOutputFile = open(OutputLogDirectory + "\\" + EV_type + '_' + LogFilesList[i] + '.txt', "w")
        Ev_op_name = EvtOutputFile.write(EventLog.to_asn1())
        CheckMsgPresence(OutputLogDirectory + "\\" + EV_type + '_' + LogFilesList[i] + '.txt')
        EvtOutputFile.close()
        HTrigger = GetEvent_HostTrigger(EventLog)
        Evt_Lat = GetEvent_HostTLatitude(EventLog)
        Evt_Long = GetEvent_HostLongitude(EventLog)
        Evt_Speed = GetEvent_HostSpeed(EventLog)
        Evt_Sequence = GetEvent_SeqNo(EventLog)
        Evt_df = pd.DataFrame({'Sequence_No':Evt_Sequence, 'Latitude':Evt_Lat, 'Longitude':Evt_Long, 'Speed_mph':Evt_Speed})
        # Normalizing the Event data for location & speed
        # Speed multiply by Spd_Factor
        # Location divide by Loc_Factor
        Evt_df['Latitude'] = Evt_df['Latitude'].apply(lambda x: x / Loc_Factor)
        Evt_df['Longitude'] = Evt_df['Longitude'].apply(lambda x: x / Loc_Factor)
        Evt_df['Speed_mph'] = Evt_df['Speed_mph'].apply(lambda x: x * Spd_Factor)
        # Get the index of Trigger Point
        df_index = Evt_df.index[Evt_df['Sequence_No'] == HTrigger]
        #Output
        Evt_df.to_csv(OutputLogDirectory + "\\" + EV_type + '_' + LogFilesList[i] + '.csv', index=False, header=True)
        outfile = EV_type + '_' + LogFilesList[i]
        pngfile = OutputLogDirectory + "\\" + EV_type + '_' + LogFilesList[i] + '.png'
        # plotting the points
        plt.figure(figsize=(8, 8))
        plt.plot(Evt_df.Sequence_No, Evt_df.Speed_mph, color='green', linestyle='dashed', linewidth=3, marker='o', markerfacecolor='blue', markersize=12)
        # naming the x axis
        plt.xlabel('Event Sequence No')
        # naming the y axis
        plt.ylabel('Speed in mph')
        # giving a title to my graph
        plt.title('Analysis of Vehicle Speed Variation')
        # Add labels to the plot
        style = dict(size=12, color='red')
        plt.text(Evt_df.iloc[df_index]['Sequence_No'], Evt_df.iloc[df_index]['Speed_mph'], "ALERT TRIGGER", **style)
        plt.savefig(pngfile)
        #print(i, outfile, HTrigger)
        if BSMPresence:
            bsmSt = "Available"
        else:
            bsmSt = "Not Available"
        if TIMPresence:
            timSt = "Available"
        else:
            timSt = "Not Available"
        if SPATPresence:
            spatSt = "Available"
        else:
            spatSt = "Not Available"
        if MAPPresence:
            mapSt = "Available"
        else:
            mapSt = "Not Available"
        EvtSummary = EvtSummary.append({'Filename':outfile,'BSM_Count':len(Evt_Lat),'BSMList':bsmSt,'TIMList':timSt,
                                        'MAPList':mapSt,'SPATList':spatSt,'TriggerSequence':HTrigger}, ignore_index=True)
        ResetVariables()
    elif islogbc(contents) == 1:
        print("Log is BC Log")
        BCLog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDMobility
        BCLog.from_uper(contents)
        bc2kml(BCLog,LogFilesList[i])
    elif islogota(contents) == 1:
        print("Log is OTA Log")
        OTALog = ota_nyc.OTA_NYC.NycOtaPdu
        OTALog.from_uper(contents)
        OTAOutputFile = open(OutputLogDirectory + '\\' + LogFilesList[i] + '.txt', "w")
        OTAOutputFile.write(OTALog.to_asn1())
        OTAOutputFile.close()
    elif islogrf(contents) == 1:
        RFLog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDRF
        RFLog.from_uper(contents)
        find_rflog_type_and_process(RFLog, LogFilesList[i])
    else:
        print("Checking if the log is in JSON format")
        nb_logfile = open(InputLogDirectory + '\\' + LogFilesList[i], "r")
        nb_contents = nb_logfile.read()
        if islogevent_json(nb_contents) == 1:
            EventLog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdEvent
            EventLog.from_json(nb_contents)
            # Check the type of Event log
            EV_type = (ProcessEventInfo(EventLog)).upper()
            EvtOutputFile = open(OutputLogDirectory + "\\" + EV_type + '_' + LogFilesList[i] + '.txt', "w")
            Ev_op_name = EvtOutputFile.write(EventLog.to_asn1())
            CheckMsgPresence(OutputLogDirectory + "\\" + EV_type + '_' + LogFilesList[i] + '.txt')
            EvtOutputFile.close()
            HTrigger = GetEvent_HostTrigger(EventLog)
            Evt_Lat = GetEvent_HostTLatitude(EventLog)
            Evt_Long = GetEvent_HostLongitude(EventLog)
            Evt_Speed = GetEvent_HostSpeed(EventLog)
            Evt_Sequence = GetEvent_SeqNo(EventLog)
            Evt_df = pd.DataFrame(
                {'Sequence_No': Evt_Sequence, 'Latitude': Evt_Lat, 'Longitude': Evt_Long, 'Speed_mph': Evt_Speed})
            # Normalizing the Event data for location & speed
            # Speed multiply by Spd_Factor
            # Location divide by Loc_Factor
            Evt_df['Latitude'] = Evt_df['Latitude'].apply(lambda x: x / Loc_Factor)
            Evt_df['Longitude'] = Evt_df['Longitude'].apply(lambda x: x / Loc_Factor)
            Evt_df['Speed_mph'] = Evt_df['Speed_mph'].apply(lambda x: x * Spd_Factor)
            # Get the index of Trigger Point
            df_index = Evt_df.index[Evt_df['Sequence_No'] == HTrigger]
            # Output
            Evt_df.to_csv(OutputLogDirectory + "\\" + EV_type + '_' + LogFilesList[i] + '.csv', index=False,
                          header=True)
            outfile = EV_type + '_' + LogFilesList[i]
            pngfile = OutputLogDirectory + "\\" + EV_type + '_' + LogFilesList[i] + '.png'
            # plotting the points
            plt.figure(figsize=(8, 8))
            plt.plot(Evt_df.Sequence_No, Evt_df.Speed_mph, color='green', linestyle='dashed', linewidth=3, marker='o',
                     markerfacecolor='blue', markersize=12)
            # naming the x axis
            plt.xlabel('Event Sequence No')
            # naming the y axis
            plt.ylabel('Speed in mph')
            # giving a title to my graph
            plt.title('Analysis of Vehicle Speed Variation')
            # Add labels to the plot
            style = dict(size=12, color='red')
            plt.text(Evt_df.iloc[df_index]['Sequence_No'], Evt_df.iloc[df_index]['Speed_mph'], "ALERT TRIGGER", **style)
            plt.savefig(pngfile)
            # print(i, outfile, HTrigger)
            if BSMPresence:
                bsmSt = "Available"
            else:
                bsmSt = "Not Available"
            if TIMPresence:
                timSt = "Available"
            else:
                timSt = "Not Available"
            if SPATPresence:
                spatSt = "Available"
            else:
                spatSt = "Not Available"
            if MAPPresence:
                mapSt = "Available"
            else:
                mapSt = "Not Available"
            EvtSummary = EvtSummary.append(
                {'Filename': outfile, 'BSM_Count': len(Evt_Lat), 'BSMList': bsmSt, 'TIMList': timSt,
                 'MAPList': mapSt, 'SPATList': spatSt, 'TriggerSequence': HTrigger}, ignore_index=True)
            ResetVariables()
        elif islogbc_json(nb_contents) == 1:
            print("Log is BC Log in JSON Format")
            BCLog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDMobility
            BCLog.from_json(nb_contents)
            bc2kml(BCLog, LogFilesList[i])
        elif islogota_json(nb_contents) == 1:
            print("Log is OTA Log in JSON Format")
            OTALog = ota_nyc.OTA_NYC.NycOtaPdu
            OTALog.from_json(nb_contents)
            OTAOutputFile = open(OutputLogDirectory + '\\' + LogFilesList[i] + '.txt', "w")
            OTAOutputFile.write(OTALog.to_asn1())
            OTAOutputFile.close()
        elif islogrf_json(nb_contents) == 1:
            print("Log is RF Log in JSON Format")
            RFLog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdASDRF
            RFLog.from_json(nb_contents)
            find_rflog_type_and_process(RFLog, LogFilesList[i])
        else:
            print("Unsupported Log / Unsupported Log Type")
EvtSummary.to_csv(OutputLogDirectory + "\\" + "Report" + '_' + "EventLogs" + '.csv', index=True, header=True)