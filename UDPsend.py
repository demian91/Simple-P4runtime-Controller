#!/usr/bin/python

from scapy.all import *
import argparse


def main():
    """
    """
    #packet = IP(dst="10.7.100.10")/TCP()/"from scapy packet"
    #send(packet)


def packet_with_seq_n(port):
    packet = Ether(src="3c:a8:2a:13:8f:bb", dst="00:04:00:00:00:01")/IP(dst="10.10.3.3", src="10.10.10.1")/UDP(sport=7777, dport=port)/"111111112222222233333333"
    sendp(packet, iface="eth0")

if __name__ == "__main__":
    main()
    parser = argparse.ArgumentParser(description='Simple script that sends TCP packets to an interface using scapy package')
    parser.add_argument('--dst-port', help='Destination port', type=int, action="store",    default=80)
    args = parser.parse_args()
    for i in range(0, 5):
        packet_with_seq_n(int(args.dst_port))

