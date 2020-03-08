import time
import socket

FILE = "samplehex.hex"
Length = 1299

def main():
    index = 0
    f=open(FILE, "r")

with open(FILE, 'rb') as infile:
    while True:
        data = infile.read(1299)
        print(data)
        if data:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.settimeout(1.0)
            addr = ("127.0.0.1", 12000)
            client_socket.sendto(data, addr)
        if not data:
            break # we have reached …

if __name__== "__main__":
  main()
