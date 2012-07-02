#!/usr/bin/env python2.7

import os
import sys
from scapy.all import *
import time
import datetime

if __name__ == "__main__":
    pcap_input_filepath = sys.argv[1]
    pcap_input_filepath_2 = sys.argv[2]
    udp_sip = sys.argv[3]
    udp_sport = int(sys.argv[4])
    udp_dip = sys.argv[5]
    udp_dport = int(sys.argv[6])
    assert(os.path.isfile(pcap_input_filepath))
    assert(os.path.isfile(pcap_input_filepath_2))
    for input_filepath in [pcap_input_filepath, pcap_input_filepath_2]:
        print '-' * 79
        print "sending: %s at %s" % (input_filepath, datetime.datetime.now().isoformat())
        print '-' * 79
        reader = PcapReader(input_filepath)
        try:
            while True:
                packet = reader.read_packet()
                if packet is None:
                    break
                packet[UDP].decode_payload_as(RTP)
                packet_to_send = IP(src=udp_sip, dst=udp_dip) / UDP(sport=udp_sport, dport=udp_dport) / packet[RTP]
                send(packet_to_send)
                time.sleep(0.02)
        finally:
            reader.close()

