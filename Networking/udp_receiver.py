import time
import socket

FILE = "test.bin"

def fileread():
    index = 0
    Length = 0
    contents = []
    f=open(FILE, "r")
    if f.mode == 'r':
       contents =f.read().splitlines()
       Length = len(contents)
    while index < Length:
            print("Item index :", index, "Content:", contents[index])
            index += 1

for pings in range(10):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)
    message = b'test'
    addr = ("127.0.0.1", 12000)

    start = time.time()
    client_socket.sendto(message, addr)
    try:
        data, server = client_socket.recvfrom(1024)
        end = time.time()
        elapsed = end - start
        print(f'{data} {pings} {elapsed}')
    except socket.timeout:
        print('REQUEST TIMED OUT')

def main():
    fileread()

if __name__== "__main__":
  main()