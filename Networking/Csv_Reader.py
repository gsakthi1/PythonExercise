
# importing the requests library 
import requests
import json
import csv
  
# api-endpoint 
URL = "https://vision.danlawinc.com/webapi/FOTA/fileToDownLoad"

#Request Parameters
PARAMS = {'token':'897eeb1647a20d231c62a16d61b73dd6b1b618984f5bc867e2635e9a65f9fcb447e9555f3ce40fcb4fa1cc354e93ffbb',
          'appCode':'V2X_ASD',
          'serialNo':'0011223344'} 

SerialNo = csv.reader(open("Serial_1157.csv"))
Prefix = '00'
index = 0
pendingIndex = 0

#Open a new CSV file
with open('Servr_Rsp.csv', mode='w') as csv_file:
    fieldname = ['SerialNo', 'fileName']
    writer = csv.DictWriter(csv_file, fieldnames=fieldname)
    writer.writeheader()
            
for row in SerialNo:
    NewSerial = Prefix + str(row)[2:10]
    PARAMS['serialNo'] = str(NewSerial)
    print("Row Index:", index, "-" , PARAMS['serialNo'])
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS) 
    data = r.json()
#    print(data)
    index += 1
    if (r.status_code == 200 and data["status"]=="success"):
        # extracting data in json format 
#        print("OTA File Name:", data["data"]["FOTA_parameters"]["fileName"])
#        print("No Of Bytes:", data["data"]["FOTA_parameters"]["fileSize"])
#        print("File Checksum:", data["data"]["FOTA_parameters"]["fileChecksum"])
#        Append data to the CSV file
        with open('Servr_Rsp.csv', mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldname)
            d = {'SerialNo': PARAMS['serialNo'],'fileName':data["data"]["FOTA_parameters"]["fileName"]}
            writer.writerow(d)
    else:
            pendingIndex += 1
            with open('Servr_Rsp.csv', mode='a') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldname)
                d = {'SerialNo': PARAMS['serialNo'],'fileName':data["error"]}
                writer.writerow(d)
            print("Request Error -  ", data["error"], " Pending Index - ", pendingIndex)
    
