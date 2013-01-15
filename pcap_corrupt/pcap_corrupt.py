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
        packet[UDP].decode_payload_as(RTP)
        packet[RTP].sequence = random.randint(0, 65535)
        output_packets.append(packet)
    return output_packets

def transform_by_set_sequence_number_to_zero(input_packets):
    logger = logging.getLogger("%s.transform_by_set_sequence_number_to_zero" % (APP_NAME, ))
    logger.debug("entry.")
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)
        packet[RTP].sequence = 0
        output_packets.append(packet)
    return output_packets

def transform_by_reverse_sequence_numbers(input_packets):
    logger = logging.getLogger("%s.transform_by_reverse_sequence_numbers" % (APP_NAME, ))
    logger.debug("entry.")
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)
    sequence_numbers = [packet[UDP].sequence for packet in input_packets]
    sequence_numbers.reverse()
    for packet, sequence_number in zip(input_packets, sequence_numbers):
        packet[RTP].sequence = sequence_number
        output_packets.append(packet)
    return output_packets

def transform_by_reverse_chunk_of_sequence_numbers(input_packets):
    logger = logging.getLogger("%s.transform_by_reverse_chunk_of_sequence_numbers" % (APP_NAME, ))
    logger.debug("entry.")
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)

    all_sequence_numbers = [packet[UDP].sequence for packet in input_packets]
    ten_percent = int(0.1 * len(all_sequence_numbers))
    start_index = random.randint(0, len(all_sequence_numbers) - ten_percent - 2)
    end_index = start_index + 1 + ten_percent
    subset_sequence_numbers = all_sequence_numbers[start_index:end_index+1]
    subset_sequence_numbers.reverse()
    all_sequence_numbers[start_index:end_index+1] = subset_sequence_numbers

    for packet, sequence_number in zip(input_packets, all_sequence_numbers):
        packet[RTP].sequence = sequence_number
        output_packets.append(packet)
    return output_packets

def transform_by_swap_pairs_of_sequence_numbers(input_packets, separation=1):
    logger = logging.getLogger("%s.transform_by_swap_adjacent_pairs_of_sequence_numbers" % (APP_NAME, ))
    logger.debug("entry. separation: %s" % (separation, ))
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)

    all_sequence_numbers = [packet[UDP].sequence for packet in input_packets]
    ten_percent = int(0.1 * len(all_sequence_numbers))
    for i in xrange(ten_percent):
        random_index = random.randint(0, len(all_sequence_numbers) - 1 - separation)
        next_index = random_index + separation
        all_sequence_numbers[random_index], all_sequence_numbers[next_index] = all_sequence_numbers[next_index], all_sequence_numbers[random_index]

    for packet, sequence_number in zip(input_packets, all_sequence_numbers):
        packet[RTP].sequence = sequence_number
        output_packets.append(packet)
    return output_packets

def transform_by_swap_adjacent_pairs_of_sequence_numbers(input_packets):
    return transform_by_swap_pairs_of_sequence_numbers(input_packets, separation=1)

def transform_by_swap_one_off_pairs_of_sequence_numbers(input_packets):
    return transform_by_swap_pairs_of_sequence_numbers(input_packets, separation=2)

def transform_by_swap_two_off_pairs_of_sequence_numbers(input_packets):
    return transform_by_swap_pairs_of_sequence_numbers(input_packets, separation=3)

def transform_by_apply_jitter_to_sequence_numbers(input_packets):
    logger = logging.getLogger("%s.transform_by_apply_jitter_to_sequence_numbers" % (APP_NAME, ))
    logger.debug("entry.")
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)
    sequence_numbers = [packet[UDP].sequence for packet in input_packets]
    interval = 3
    proportion = 0.1
    for packet, sequence_number in zip(input_packets, sequence_numbers):
        if random.random() < proportion:
            packet[RTP].sequence = random.randint(sequence_number - interval, sequence_number + interval)
        output_packets.append(packet)
    return output_packets

def transform_by_randomise_timestamps(input_packets):
    logger = logging.getLogger("%s.transform_by_randomise_timestamps" % (APP_NAME, ))
    logger.debug("entry.")
    output_packets = []
    minimum_timestamp = 0
    maximum_timestamp = 2 ** 32 - 1
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)
        packet[RTP].timestamp = random.randint(minimum_timestamp, maximum_timestamp)
        output_packets.append(packet)
    return output_packets

def transform_by_set_zero_timestamps(input_packets):
    logger = logging.getLogger("%s.transform_by_set_zero_timestamps" % (APP_NAME, ))
    logger.debug("entry.")
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)
        packet[RTP].timestamp = 0
        output_packets.append(packet)
    return output_packets

def transform_by_reverse_timestamps(input_packets):
    logger = logging.getLogger("%s.transform_by_reverse_timestamps" % (APP_NAME, ))
    logger.debug("entry.")
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)
    timestamps = [packet[RTP].timestamp for packet in input_packets]
    timestamps.reverse()
    for packet, timestamp in zip(input_packets, timestamps):
        packet[RTP].timestamp = timestamp
        output_packets.append(packet)
    return output_packets

def transform_by_reverse_chunk_of_timestamps(input_packets):
    logger = logging.getLogger("%s.transform_by_reverse_chunk_of_timestamps" % (APP_NAME, ))
    logger.debug("entry.")
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)

    all_timestamps = [packet[RTP].timestamp for packet in input_packets]
    ten_percent = int(0.1 * len(all_timestamps))
    start_index = random.randint(0, len(all_timestamps) - ten_percent - 2)
    end_index = start_index + 1 + ten_percent
    subset_timestamps = all_timestamps[start_index:end_index+1]
    subset_timestamps.reverse()
    all_timestamps[start_index:end_index+1] = subset_timestamps

    for packet, timestamp in zip(input_packets, all_timestamps):
        packet[RTP].timestamp = timestamp
        output_packets.append(packet)
    return output_packets

def transform_by_apply_jitter_to_timestamps(input_packets):
    logger = logging.getLogger("%s.transform_by_apply_jitter_to_timestamps" % (APP_NAME, ))
    logger.debug("entry.")
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)
    timestamps = [packet[RTP].timestamp for packet in input_packets]

    # The timestamp is incremented by the packetization interval * the sampling rate
    # For example, 20ms audio sampled at 8,000 Hz = 160.
    base_interval = 160 # assume 20ms audio sampled at 8,000 Hz.
    interval = base_interval * 10
    proportion = 0.1
    minimum_timestamp = 0
    maximum_timestamp = 2 ** 32 - 1
    for packet, timestamp in zip(input_packets, timestamps):
        if random.random() < proportion:
            new_timestamp = random.randint(timestamp - interval, timestamp + interval)
            new_timestamp = max(minimum_timestamp, new_timestamp)
            new_timestamp = min(maximum_timestamp, new_timestamp)
            packet[RTP].timestamp = new_timestamp
        output_packets.append(packet)
    return output_packets

def transform_by_swap_pairs_of_timestamps(input_packets, separation=1):
    logger = logging.getLogger("%s.transform_by_swap_adjacent_pairs_of_timestamps" % (APP_NAME, ))
    logger.debug("entry. separation: %s" % (separation, ))
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)

    all_timestamps = [packet[RTP].timestamp for packet in input_packets]
    ten_percent = int(0.1 * len(all_timestamps))
    for i in xrange(ten_percent):
        random_index = random.randint(0, len(all_timestamps) - 1 - separation)
        next_index = random_index + separation
        all_timestamps[random_index], all_timestamps[next_index] = all_timestamps[next_index], all_timestamps[random_index]

    for packet, timestamp in zip(input_packets, all_timestamps):
        packet[RTP].timestamp = timestamp
        output_packets.append(packet)
    return output_packets

def transform_by_swap_adjacent_pairs_of_timestamps(input_packets):
    return transform_by_swap_pairs_of_timestamps(input_packets, separation=1)

def transform_by_swap_one_off_pairs_of_timestamps(input_packets):
    return transform_by_swap_pairs_of_timestamps(input_packets, separation=2)

def transform_by_swap_two_off_pairs_of_timestamps(input_packets):
    return transform_by_swap_pairs_of_timestamps(input_packets, separation=3)

def transform_by_flip_bits_in_rtp_payload(input_packets, proportion=0.01):
    logger = logging.getLogger("%s.transform_by_flip_bits_in_rtp_payload" % (APP_NAME, ))
    logger.debug("entry. proportion: %s" % (proportion, ))
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)
        packet[Raw] = corrupt_bits(str(packet[Raw]), proportion)
        output_packets.append(packet)
    return output_packets

def transform_by_flip_one_percent_bits_in_payload(input_packets):
    return transform_by_flip_bits_in_rtp_payload(input_packets, proportion = 0.01)

def transform_by_flip_five_percent_bits_in_payload(input_packets):
    return transform_by_flip_bits_in_rtp_payload(input_packets, proportion = 0.05)

def transform_by_flip_ten_percent_bits_in_payload(input_packets):
    return transform_by_flip_bits_in_rtp_payload(input_packets, proportion = 0.1)

def transform_by_flip_bits_in_rtp_packet(input_packets, proportion):
    logger = logging.getLogger("%s.transform_by_flip_bits_in_rtp_packet" % (APP_NAME, ))
    logger.debug("entry. proportion: %s" % (proportion, ))
    output_packets = []
    for packet in input_packets:
        packet[UDP].decode_payload_as(RTP)
        packet[RTP] = corrupt_bits(str(packet[RTP]), proportion)
        output_packets.append(packet)
    return output_packets

def transform_by_flip_one_percent_bits_in_rtp_packet(input_packets):
    return transform_by_flip_bits_in_rtp_packet(input_packets, proportion = 0.01)

def transform_by_flip_five_percent_bits_in_rtp_packet(input_packets):
    return transform_by_flip_bits_in_rtp_packet(input_packets, proportion = 0.05)

def transform_by_flip_ten_percent_bits_in_rtp_packet(input_packets):
    return transform_by_flip_bits_in_rtp_packet(input_packets, proportion = 0.1)

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

    for function in [ \
                     transform_by_randomise_sequence_numbers,
                     transform_by_set_sequence_number_to_zero,
                     transform_by_reverse_sequence_numbers,
                     transform_by_reverse_chunk_of_sequence_numbers,
                     transform_by_swap_adjacent_pairs_of_sequence_numbers,
                     transform_by_swap_one_off_pairs_of_sequence_numbers,
                     transform_by_swap_two_off_pairs_of_sequence_numbers,
                     transform_by_apply_jitter_to_sequence_numbers,
                     transform_by_randomise_timestamps,
                     transform_by_set_zero_timestamps,
                     transform_by_reverse_timestamps,
                     transform_by_reverse_chunk_of_timestamps,
                     transform_by_apply_jitter_to_timestamps,
                     transform_by_swap_adjacent_pairs_of_timestamps,
                     transform_by_swap_one_off_pairs_of_timestamps,
                     transform_by_swap_two_off_pairs_of_timestamps,
                     transform_by_flip_one_percent_bits_in_payload,
                     transform_by_flip_five_percent_bits_in_payload,
                     transform_by_flip_ten_percent_bits_in_payload,
                     transform_by_flip_one_percent_bits_in_rtp_packet,
                     transform_by_flip_five_percent_bits_in_rtp_packet,
                     transform_by_flip_ten_percent_bits_in_rtp_packet,
                     ]:
        apply_transform(function, pcap_input_filepath)

if __name__ == "__main__":
    logger.info("starting")
    random_seed = "OWMzZTRhZTU2Y2Q4NGMyMzg2ZmRmMTI2MjFiMjQwNzIwZWJlZjRmNTNmMzk0NGI3YjdhMTA3N2Y0MThkMjcxOQ"
    logger.debug("random_seed: %s" % (random_seed, ))
    random.seed(random_seed)
    main(pcap_input_filepath = r"/root/ai/sipp/g711a.pcap")

