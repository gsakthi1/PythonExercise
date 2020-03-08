
# importing the requests library 
import requests
import json
  
# defining the api-endpoint  
URL_1 = "https://visioninternal.danlawinc.com/webapi/Logger/submit_A_Log"
URL_2 = "https://visioninternal.danlawinc.com/webapi/FOTA/updateStatus"

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# data to be sent to api 
PARAMS = {'token':'897eeb1647a20d231c62a16d61b73dd6b1b618984f5bc867e2635e9a65f9fcb447e9555f3ce40fcb4fa1cc354e93ffbb', 
        'appCode':'V2X_ASD','logType':'health',
         'data':{'serialNo':"0016201901",'UTC':46,'currentVersion':'01.8.4','faultCode':10,'rsuLocation':10}}

json_data = json.dumps(PARAMS)

#print(PARAMS['token'])
#print(PARAMS['data']['serialNo'])
#print(PARAMS['data']['UTC'])
#print(PARAMS['data']['currentVersion'])
#print(PARAMS['data']['faultCode'])
print(json_data)

# sending post request and saving response as response object 
#r = requests.post(url = URL_1, params=json_data, headers=headers)
#print("The Response Params: ", r.text)

r = requests.post(URL_1, json=json_data, headers=headers)
print("The Response json: ", r.status_code) 

########################################################################

# data to be sent to api 
#PARAMS_2 = {'token':'897eeb1647a20d231c62a16d61b73dd6b1b618984f5bc867e2635e9a65f9fcb447e9555f3ce40fcb4fa1cc354e93ffbb', 
#        'appCode':'V2X_ASD','logType':'otastatus','newStatus':'FAIL', 'serialNo':'0016001901'}
#json_data_2 = json.dumps(PARAMS_2)

#r_2 = requests.post(url = URL_2, json={'token':'897eeb1647a20d231c62a16d61b73dd6b1b618984f5bc867e2635e9a65f9fcb447e9555f3ce40fcb4fa1cc354e93ffbb', 
#        'appCode':'V2X_ASD','logType':'otastatus','newStatus':'FAIL', 'serialNo':'0016001901'})
  
# extracting response text  
#pastebin_url_2 = r_2.text 
#print("The pastebin URL is:%s"%pastebin_url_2) 
