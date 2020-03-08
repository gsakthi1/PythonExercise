import socket
import argparse
import os
import sys
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP, UDP

FILENAME = 'udp_2924.pcap'
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
global message

def process_pcap(file_name):
    print('Opening {}...'.format(file_name))
    count = 0
    interesting_packet_count = 0
    
    for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
        count += 1
        message = (pkt_data[144:-4].hex())
        print((message[0]))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, (UDP_IP, UDP_PORT))


if __name__ == '__main__':  
    process_pcap(FILENAME)
    sys.exit(0)
    


