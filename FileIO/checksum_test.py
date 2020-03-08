import time
import socket

FILE = "hexinput.hex"
index = 2

def main():
    f=open(FILE, "r")

with open(FILE, 'rb') as infile:
    byte = infile.read(1)
    byte_1 = infile.read(1)
    
    print(byte)
    Csum = bin((int(byte,2)+int(byte_1,2))
    print(byte)
               
#    print("First : ", Csum)
#    byte = 0
#    while byte != b"":
#        byte = infile.read(1)
#        Csum += byte
#        print("Second : ", Csum)
#        byte = 0

if __name__== "__main__":
  main()
