# importing the requests library
import csv
import pandas as pd
import datetime
from datetime import date

Custfile = 'Umtri_Serial_Input.csv'
Outfile = '2019_349_ServerMapping_Jan_Aug_03.csv'
Inputfile = '2019_LogReport.csv'

DeviceFound = 0
ts_epoch = 0
ts_utc = 0
Prefix = '00'

df1 = pd.read_csv(Inputfile)
server_data = df1[["Date & Time", "Serial No", "Current Version"]]
customer_data = pd.read_csv(Custfile)
df_out = pd.DataFrame({"SerialNo": [0], "CurrSW": [0], "TimeStamp": [0]})

for j in range(len(customer_data)):
    DeviceFound = 0
    print("Serial Entry - ",j)
    for i in range(len(server_data)) :
      #NewSerial = Prefix + str(customer_data.loc[j,"serialNo"])    #2020 Check
      NewSerial = str(customer_data.loc[j, "serialNo"])            #2019 Check
      #print(i,server_data.loc[i, "Serial No"], NewSerial)
      if(server_data.loc[i, "Serial No"] == NewSerial):
          #print(j,"ASD Found", customer_data.loc[j,"serialNo"], server_data.loc[i, "Date & Time"],server_data.loc[i, "Current Version"])
          #df_out.append([customer_data.loc[j,"serialNo"],server_data.loc[i, "Current Version"],server_data.loc[i, "Date & Time"]])
          ts_epoch = int(float(server_data.loc[i, "Date & Time"]))
          print(ts_epoch)
          ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')
          df_out.loc[j,"SerialNo"] = customer_data.loc[j,"serialNo"]
          df_out.loc[j,"CurrSW"] = server_data.loc[i,"Current Version"]
          df_out.loc[j,"TimeStamp"] = ts
          DeviceFound = 1
          break
    #print(server_data.loc[i, "Serial No"], customer_data.loc[j,"serialNo"])
    #print(j,"ASD Missing", customer_data.loc[2,"serialNo"])
    if(DeviceFound == 0):
        df_out.loc[j,"SerialNo"] = customer_data.loc[j,"serialNo"]
        df_out.loc[j,"CurrSW"] = "No data available in server"
        df_out.loc[j,"TimeStamp"] = "No data available in server"
#print(df_out)
df_out.to_csv(Outfile)