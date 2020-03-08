
# Python 3 code to demonstrate theworking of MD5 
  
import hashlib
import os
  
result = hashlib.md5(open('16720_1.tar.gz','rb').read()).hexdigest()
size = os.path.getsize('16720_1.tar.gz')
print("MD5sum of 16720_1.tar.gz :", result, "Length :" , size) 

result = hashlib.md5(open('16720_3.tar.gz','rb').read()).hexdigest()
size = os.path.getsize('16720_3.tar.gz')
print("MD5sum of 16720_3.tar.gz :", result, "Length :" , size) 

result = hashlib.md5(open('16720_5.tar.gz','rb').read()).hexdigest()
size = os.path.getsize('16720_5.tar.gz')
print("MD5sum of 16720_5.tar.gz :", result, "Length :" , size) 
