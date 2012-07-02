#!/usr/bin/env python2.7

import os
import sys
import random

from scapy.all import *

# -----------------------------------------------------------------------------
#   Constants.
# -----------------------------------------------------------------------------
APP_NAME = "pcap_corrupt"
LOG_PATH = r"/var/log/"
LOG_FILENAME = r"/var/log/pcap_corrupt.log"
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
#   Logging.
# -----------------------------------------------------------------------------
import logging, logging.handlers
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
if not os.path.isdir(LOG_PATH):
    os.makedirs(LOG_PATH)
ch2 = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10*1024*1024, backupCount=10)
ch2.setFormatter(formatter)
logger.addHandler(ch2)
logger = logging.getLogger(APP_NAME)
# -----------------------------------------------------------------------------

def transform_by_randomise_sequence_numbers(input_packets):
    logger = logging.getLogger("%s.transform_by_randomise_sequence_numbers" % (APP_NAME, ))
    logger.debug("entry.")
    output_packets = []
    for packet in input_packets:
        #output_packet = packet
        #output_packet = packet.copy()
        packet[UDP].decode_payload_as(RTP)
        #raw = str(packet[Raw])
        #rtp = RTP(raw)
        packet[RTP].sequence = random.randint(0, 65535)
        #import pdb; pdb.set_trace()
        #packet[RTP].decode_payload_as(Raw)
        #import pdb; pdb.set_trace()
        #output_packet[Raw] = str(rtp)
        #output_packet = Ether() / IP() / UDP() / RTP()
        output_packets.append(packet)
    return output_packets

def get_output_filepath(transform_function, pcap_input_filepath):
    logger = logging.getLogger("%s.get_output_filepath" % (APP_NAME, ))
    logger.debug("entry. transform_function: %s, pcap_input_filepath: %s" % (transform_function, pcap_input_filepath))
    head, tail = os.path.split(pcap_input_filepath)
    filename, dot, fileext = tail.partition(".")
    output_filename = filename + "_" + transform_function.__name__.partition("transform_by_")[-1]
    pcap_output_filepath = os.path.join(head, output_filename + "." + fileext)
    logger.debug("returning: %s" % (pcap_output_filepath, ))
    return pcap_output_filepath

def apply_transform(transform_function, pcap_input_filepath):
    logger = logging.getLogger("%s.apply_transform" % (APP_NAME, ))
    logger.debug("entry. transform_function: %s, pcap_input_filepath: %s" % (transform_function, pcap_input_filepath))
    pcap_output_filepath = get_output_filepath(transform_function, pcap_input_filepath)
    reader = PcapReader(pcap_input_filepath)
    input_packets = [packet for packet in reader.read_all(count=-1)]
    reader.close()
    output_packets = transform_function(input_packets)
    writer = PcapWriter(pcap_output_filepath)
    writer.write(output_packets)
    writer.close()

def main(pcap_input_filepath):
    logger = logging.getLogger("%s.main" % (APP_NAME, ))
    logger.debug("entry. pcap_input_filepath: %s" % (pcap_input_filepath, ))

    apply_transform(transform_by_randomise_sequence_numbers, pcap_input_filepath)

if __name__ == "__main__":
    logger.info("starting")
    random_seed = "OWMzZTRhZTU2Y2Q4NGMyMzg2ZmRmMTI2MjFiMjQwNzIwZWJlZjRmNTNmMzk0NGI3YjdhMTA3N2Y0MThkMjcxOQ"
    logger.debug("random_seed: %s" % (random_seed, ))
    random.seed(random_seed)
    main(pcap_input_filepath = r"/root/ai/sipp/g711a.pcap")

