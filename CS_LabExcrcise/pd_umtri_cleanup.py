import pandas as pd
import numpy as np
import time
import sys
import matplotlib.pyplot as plt

filename = "Umtri_2019_input.csv"
output = "Umtri_2019_output.csv"

df=pd.read_csv(filename)

#print(df.head())
print(df.columns)

missing_data_0 = df.isnull()
#Identify the missing data in each column
for column in missing_data_0.columns.values.tolist():
    print(column)
    print (missing_data_0[column].value_counts())
    print("") 

#Delete missing entry ROWS
df.dropna(subset=["Date & Time"], axis = 0, inplace = True)    
df.dropna(subset=["Serial No"], axis = 0, inplace = True)    
df.dropna(subset=["Current Version"], axis = 0, inplace = True)    
df.dropna(subset=["Fault Code"], axis = 0, inplace = True)    
df.dropna(subset=["Rsu Location"], axis = 0, inplace = True)
df.reset_index(drop=True, inplace=True)

print("------ Cleaned up data - ----")
missing_data_1 = df.isnull()
#Identify the missing data in each column
for column in missing_data_1.columns.values.tolist():
    print(column)
    print (missing_data_1[column].value_counts())
    print("") 

#df["Date & Time"] = df["Date & Time"].astype("int")
#print(df.dtypes) # List all data types of data frame

df.drop(columns=['Rsu Location'], inplace = True)
options = ['ASD-SW_v1.8.3','ASD-SW_v1.8.4','ASD_OTA-SW_v1.0','ASD_OTA-SW_v1.1']

#df_183 = df.loc[df['Current Version'] == 'ASD-SW_v1.8.3']
#df_184 = df.loc[df['Current Version'] == 'ASD-SW_v1.8.4']
#df_ota10  = df.loc[df['Current Version'] == 'ASD_OTA-SW_v1.0']
#df_ota11  = df.loc[df['Current Version'] == 'ASD_OTA-SW_v1.1']
#df_filtered_0 = pd.concat([df_183,df_184], axis=1)
#df_filtered_1 = pd.concat([df_183,df_184], axis=1)
#df_filtered_2 = pd.concat([df_filtered_0,df_filtered_1], axis=1)

print("------ RSU Location dropped data - ----")

df_options = df[df['Current Version'].isin(options)]
df_options.reset_index(inplace = True)

print("------ Valid SW version data - ----")

#df_filtered = df[df['Current Version'] != 'ASD_OTA-SW_v1.0'] or df[df['Current Version'] != 'ASD-SW_v1.8.4'] or df[df['Current Version'] != 'ASD-SW_v1.8.3'] or df[df['Current Version'] != 'ASD_OTA-SW_v1.1']
#print(df_filtered.head())
#Convert EPOCH time to timestamp
#df['TimeStamp'] = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(df['Date & Time']))
#df_filtered_2.to_csv('Filtered_umtri.csv')

df_options.to_csv(output)
#print(df_options.info)
#print(df_options.dtypes)

#epoch = df_options['Date & Time'][1]
#t_data = time.strftime("%d %b %Y", time.localtime(int(epoch)))
#print(t_data)

#time_data = time.strftime("%b", time.localtime(int(df_options['Date & Time'][1])))
#print(time_data)

srl = df_options['Serial No'].value_counts()
Cvsion = df_options['Current Version'].value_counts()

MonthInfo = df_options['Date & Time']
MonthLen = len(MonthInfo)
MonthDataList = []
#print(len(MonthInfo), MonthInfo.size)


for i in range(0,MonthLen):
    time_data = time.strftime("%b", time.localtime(int(df_options['Date & Time'][i])))
    MonthDataList.append(time_data)

#print(len(MonthDataList))
    
print("------ Merging Serial & Month Data - ----")

serial_list = df_options['Serial No']
df_month = pd.DataFrame(MonthDataList)
df_serial = pd.DataFrame(serial_list)
#print(df_month.tail())
#print(df_serial.tail())

print("------ Merged Data Serial & Month Data - ----")
df_serial['Month'] = df_month
print(df_serial.head())
print(df_serial.dtypes)
print(df_serial['Month'].value_counts())
print(df_serial['Serial No'].value_counts())

df_serial.to_csv('Umtri_final_op.csv')
df_serial['Serial No'].value_counts().reset_index().to_csv('Umtri_SerialFreq.csv')
df_serial['Month'].value_counts().reset_index().to_csv('Umtri_MonthFreq.csv')

#''''''''''''''''''''''
print(df_serial.describe(include=['object']))

