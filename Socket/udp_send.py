import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)

#file=open("samplehex.hex","r",)
#for line in file:
#    line = line.rstrip('\n')
#    arr = bytearray(line, 'utf-8')
#    print(arr)
#    print("Length  - ", len(line))
#    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    sock.sendto(arr[:1299], (UDP_IP, UDP_PORT))
    

with open("Ascii_udp_2924_noCR.bin", 'rb') as infile:
    while True:
        data = infile.read(1299)
        print(len(data))
        if data:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = ("127.0.0.1", 12000)
            client_socket.sendto(data, (UDP_IP, UDP_PORT))
        if not data:
            break # we have reached …

