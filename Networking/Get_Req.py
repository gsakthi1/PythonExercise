
# importing the requests library 
import requests
import json
  
# api-endpoint 
URL = "https://vision.danlawinc.com/webapi/FOTA/fileToDownLoad"
  
# "UMTRI OTA - File Download Check"
  
# defining a params dict for the parameters to be sent to the API 
PARAMS = {'token':'897eeb1647a20d231c62a16d61b73dd6b1b618984f5bc867e2635e9a65f9fcb447e9555f3ce40fcb4fa1cc354e93ffbb',
          'appCode':'V2X_ASD',
          'serialNo':'0018060081'} 
  
# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
data = r.json()

if (r.status_code == 200 and data["status"]=="success"):
    # extracting data in json format 
    print("OTA File Name:", data["data"]["FOTA_parameters"]["fileName"])
    print("No Of Bytes:", data["data"]["FOTA_parameters"]["fileSize"])
    print("File Checksum:", data["data"]["FOTA_parameters"]["fileChecksum"])
else:
    print("Request Error -  ", data["error"])
    

URL_1 = "https://vision.danlawinc.com/webapi/Logger/submit_A_Log"
PARAMS_1 = {'token':'897eeb1647a20d231c62a16d61b73dd6b1b618984f5bc867e2635e9a65f9fcb447e9555f3ce40fcb4fa1cc354e93ffbb',
          'appCode':'V2X_ASD','logType':'health','data':{'serialNo':'0016201901','UTC':46,'currentVersion':'01.8.4','faultCode':10,'rsuLocation':10}} 

# sending get request and saving the response as response object 
r = requests.get(url = URL_1, json = {'token':'897eeb1647a20d231c62a16d61b73dd6b1b618984f5bc867e2635e9a65f9fcb447e9555f3ce40fcb4fa1cc354e93ffbb',
          'appCode':'V2X_ASD','logType':'health','data':{'serialNo':'0016201901','UTC':46,'currentVersion':'01.8.4','faultCode':10,'rsuLocation':10}}) 
data = r.json()
print(data)
