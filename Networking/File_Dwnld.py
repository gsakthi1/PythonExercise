
# importing the requests library 
import requests
import json
import hashlib
import os
  
# api-endpoint 
URL = "https://vision.danlawinc.com/webapi/FOTA/binaryChunk"
FileChecksum = 'd1b92ada5b1053cae20b38bafa6da566'

req = requests.post(url = URL, json = {'token':'897eeb1647a20d231c62a16d61b73dd6b1b618984f5bc867e2635e9a65f9fcb447e9555f3ce40fcb4fa1cc354e93ffbb',
          'appCode':'V2X_ASD',
          'fileName':'2019_CV2X_OTA_Test_V1.0.tgz',
          'offset' : 0,
          'sizeInBytes' : 10231})

req.raise_for_status()

with open('Download.tgz','wb')as fd:
    for chunk in req.iter_content(chunk_size=1024):
        fd.write(chunk)

#Removing the last 16 bytes from downloaded file
fp = open('Download.tgz', "rb")
content = fp.read()
fp.close()

fq = open('Xd5_Download.tgz', "wb")
fq.write(content[0:-16])
fq.close

Server_checksum = hashlib.md5(open('Download.tgz','rb').read()).hexdigest()
print('Server_checksum:', Server_checksum)
Actual_checksum = hashlib.md5(open('Xd5_Download.tgz','rb').read()).hexdigest()
print('Actual_checksum :', Actual_checksum)
server_file = os.stat('Download.tgz')
print("Server File Size: ", server_file.st_size)
actual_file = os.stat('Xd5_Download.tgz')
print("Actual File Size:", actual_file.st_size)
if(FileChecksum == Actual_checksum):
    print('Checksum Matched')
