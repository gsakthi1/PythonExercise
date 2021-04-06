'''
Example parser for Event logs.
'''


import os
from pycrate_asn1dir import J2735_NYC_03062020
from pycrate_asn1rt.utils import *
import simplekml
import pandas as pd
import matplotlib.pyplot as plt
import easygui
#V2I_Events = ['spdcomp', 'cspdomp', 'spdcompwz', 'rlvw', 'ovcturnprohibit', 'ovcclearancelimit', 'evacinfo', 'pedinxwalk', 'pedSig']

InputLogDirectory = easygui.diropenbox(msg="Select Folder with Logs for Processing", title="Input for Event", default=None)
OutputLogDirectory = InputLogDirectory+'\\'
#InputLogDirectory = "C:\\GSAKTHI_Data\\Personal_Data\\PythonExamples\\NycLogs\\LogDecryption\\Input\\EVT"
#OutputLogDirectory = "C:\\GSAKTHI_Data\\Personal_Data\\PythonExamples\\NycLogs\\Log_Output\\"
Evt_Lat =[]
Evt_Long = []
Evt_Speed = []
Evt_Sequence = []
HTrigger = 0

Loc_Factor = 10000000 # 10^-7 Degrees to Degrees
Spd_Factor = 0.02*2.23694 # 10^-2 mps to mph
Head_Factor = 0.0125
To_Radians = 0.01745329252

TIMPresence = False
MAPPresence = False
SPATPresence = False
BSMPresence = False

Evac_count = 0
Ovc_count = 0
SpdcompWz_count = 0
Rlvw_count = 0
Fcw_count = 0
Spdcmp_count = 0
Cspd_count = 0
Other_Alerts = 0

EvtSummary = pd.DataFrame(
    columns=['Filename', 'BSM_Count', 'BSMList', 'TIMList', 'MAPList', 'SPATList', 'TriggerSequence'])

LogFilesList = os.listdir(InputLogDirectory)

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

def islogevent(input_log_file):
    #print("Function that finds out if Log is Bread Crumb Log")
    dummyeventlog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdEvent
    try:
        dummyeventlog.from_uper(input_log_file)
    except:
        return 0
    else:
        return 1

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

def GetEvent_HostHeading(input_evt_file):
    dummy_heading = []
    dummy_data = get_val_at(input_evt_file, ['bsmList'])
#    print(type(dummy_data), len(dummy_data))
    for i in range(len(dummy_data)):
        dummy_heading.append(dummy_data[i]['bsmRecord']['bsmMsg']['coreData']['heading'])
    return dummy_heading

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


def CountWarningType(EV_type):
    global Ovc_count, Evac_count,Fcw_count,SpdcompWz_count,Rlvw_count,Other_Alerts,Spdcmp_count,Cspd_count
#    print("Category", EV_type)
    if EV_type == 'EVACINFO':
        Evac_count += 1
    elif EV_type == 'OVCCLEARANCELIMIT':
        Ovc_count += 1
    elif EV_type == 'FCW':
        Fcw_count += 1
    elif EV_type == 'SPDCOMPWZ':
        SpdcompWz_count += 1
    elif EV_type == 'SPDCOMP':
        Spdcmp_count += 1
    elif EV_type == 'RLVW':
        Rlvw_count += 1
    elif EV_type == 'CSPDOMP':
        Cspd_count += 1
    else:
        Other_Alerts += 1
    return

def ConverttoKml(Input,Evt_df):
    kml = simplekml.Kml()
    for ind in Evt_df.index:
        pnt = kml.newpoint(name="", coords=[(Evt_df['Longitude'][ind], Evt_df['Latitude'][ind])])
        pnt.iconstyle = simplekml.IconStyle(color=simplekml.Color.rgb(0, 255, 0), scale=0.4, heading=Evt_df['Heading'][ind] - 180,
                                        icon=simplekml.Icon(gxx=None, gxy=None, gxw=None, gxh=None,
                                                            href='http://maps.google.com/mapfiles/kml/shapes/arrow.png'),
                                        hotspot=None)
    kml.save(OutputLogDirectory + EV_type + '_' + Input + '.kml')
    return

for i in range(len(LogFilesList)):
#    print(i , "Processing File:" + LogFilesList[i])
    logfile = open(InputLogDirectory+'\\'+LogFilesList[i],"rb")
    contents =logfile.read()
    if islogevent(contents) == 1:
        EventLog = J2735_NYC_03062020.NYCEventDataUpload.NycCvpdEvent
        #Check the type of Event log
        EV_type = (ProcessEventInfo(EventLog)).upper()
        CountWarningType(EV_type)
        EvtOutputFile = open(OutputLogDirectory + EV_type + '_' + LogFilesList[i] + '.txt', "w")
        Ev_op_name = EvtOutputFile.write(EventLog.to_asn1())
        CheckMsgPresence(OutputLogDirectory + EV_type + '_' + LogFilesList[i] + '.txt')
        EvtOutputFile.close()
        HTrigger = GetEvent_HostTrigger(EventLog)
        Evt_Lat = GetEvent_HostTLatitude(EventLog)
        Evt_Long = GetEvent_HostLongitude(EventLog)
        Evt_Speed = GetEvent_HostSpeed(EventLog)
        Evt_Heading = GetEvent_HostHeading(EventLog)
        Evt_Sequence = GetEvent_SeqNo(EventLog)
        Evt_df = pd.DataFrame({'Sequence_No':Evt_Sequence, 'Latitude':Evt_Lat, 'Longitude':Evt_Long, 'Heading': Evt_Heading,'Speed_MPH':Evt_Speed})
        # Normalizing the Event data for location & speed
        # Speed multiply by Spd_Factor
        # Location divide by Loc_Factor
        Evt_df['Latitude'] = Evt_df['Latitude'].apply(lambda x: x / Loc_Factor)
        Evt_df['Longitude'] = Evt_df['Longitude'].apply(lambda x: x / Loc_Factor)
        Evt_df['Heading'] = Evt_df['Heading'].apply(lambda x: x * Head_Factor)
        Evt_df['Speed_MPH'] = Evt_df['Speed_MPH'].apply(lambda x: x * Spd_Factor)
        # Get the index of Trigger Point
        df_index = Evt_df.index[Evt_df['Sequence_No'] == HTrigger]
        # Output
        Evt_df.to_csv(OutputLogDirectory + EV_type + '_' + LogFilesList[i] + '.csv', index=False, header=True)
        # KmlOutput
        ConverttoKml(LogFilesList[i], Evt_df)
        outfile = EV_type + '_' + LogFilesList[i]
        pngfile = OutputLogDirectory + EV_type + '_' + LogFilesList[i] + '.png'
        # plotting the points
        plt.figure(figsize=(8, 8))
        plt.plot(Evt_df.Sequence_No, Evt_df.Speed_MPH, color='green', linestyle='dashed', linewidth=3,
                 marker='o', markerfacecolor='blue', markersize=12)
        # naming the x axis
        plt.xlabel('Event Sequence No')
        # naming the y axis
        plt.ylabel('Speed in MPH')
        # giving a title to my graph
        plt.title('Analysis of Vehicle Speed Variation')
        # Add labels to the plot
        style = dict(size=12, color='red')
        plt.text(Evt_df.iloc[df_index]['Sequence_No'], Evt_df.iloc[df_index]['Speed_MPH'], "WARNING ALERT TRIGGER",
                 **style)
        plt.savefig(OutputLogDirectory + EV_type + '_' + LogFilesList[i] + '.PNG')
        plt.close()
        #        print(i,outfile,HTrigger)
        EvtSummary = EvtSummary.append(
            {'Filename': outfile, 'BSM_Count': len(Evt_Lat), 'BSMList': BSMPresence, 'TIMList': TIMPresence,
             'MAPList': MAPPresence, 'SPATList': SPATPresence, 'TriggerSequence': HTrigger}, ignore_index=True)
        ResetVariables()
EvtSummary.to_csv(OutputLogDirectory + "EventLogs_ReportSummary" + '.csv', index=True, header=True)
print("Successfully Parsed Log files : ", Rlvw_count+Fcw_count+Fcw_count+Ovc_count+SpdcompWz_count+Spdcmp_count+Evac_count+Cspd_count+Other_Alerts)
print(" Valid RLVW Log Count : ",Rlvw_count)
print(" Valid FCW Log Count : ",Fcw_count)
print(" Valid OVC Log Count : ",Ovc_count)
print(" Valid EVAC Log Count :", Evac_count)
print(" Valid SPDCOMPWZ Log Count : ",SpdcompWz_count)
print(" Valid SPDCOMP Log Count : ",Spdcmp_count)
print(" Valid CSPD Log Count : ",Cspd_count)
print(" Valid Other Log Count : ",Other_Alerts)
print(" Event log summary report generated in output directory")
print("==============================================================================================")