import os
import sys
import paramiko
import select
import time
import re

import colorama
colorama.init(autoreset=True)

def strip_control_characters(input):
    if input:
        input = re.sub(r"[\x07]", "", input)
    return input

class Channel(object):
    def __init__(self, client, command, color):
        self.client = client
        self.command = command
        self.color = color
        #self.initialize()

    def initialize(self):
        print "client: %s, command: %s" % (self.client, self.command)
        self.channel = self.client.invoke_shell()
        time.sleep(3)
        self.channel.send(self.command)

def main(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    # -------------------------------------------------------------------------
    #   !!EDITME
    #
    #   Channel objects that correspond to what command output you wish
    #   to monitor. Add more channels as you wish, and then comment/add lines
    #   to the all_channels list of channels.
    #
    #   Here is a reference for what foreground colours, background colours,
    #   and styles you can have. They are bit masks, so this is valid:
    #
    #   (colorama.Fore.RED | colorama.Style.BRIGHT)
    #
    #   Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    #   Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    #   Style: DIM, NORMAL, BRIGHT, RESET_ALL
    # -------------------------------------------------------------------------
    channel_stdout = Channel(command='cdtrc && tail -f stdout\n',
                             color=(colorama.Fore.RED),
                             client=client)
    channel_messages_ngmg = Channel(command='tail -f /var/log/messages\n',
                                    color=(colorama.Fore.GREEN),
                                    client=client)
    channel_messages_solaris = Channel(command='tail -f /var/adm/messages | egrep -v "(SCTP to)"\n',
                                    color=(colorama.Fore.GREEN),
                                    client=client)
    channel_ep = Channel(command='tail -f /var/opt/MetaSwitch/ep.log\n',
                         color=(colorama.Fore.YELLOW),
                         client=client)
    channel_mslogfmt = Channel(command="mslogfmt -regexp-include 'Severity = ([6-9][0-9]|100)' -regexp-exclude '(Usage Statistics)'\n",
                               color=(colorama.Fore.MAGENTA),
                               client=client)
    channel_dcisnoop = Channel(command="dcisnoop -n '(STATS|MAN_CMD_PING|MSG_NTY_ACK)'\n",
                               color=(colorama.Fore.WHITE),
                               client=client)
    channel_apitrace = Channel(command="""/opt/MetaSwitch/util/vp3liveapitrace -V -i -t \"AIT\"\n""",
                               color=(colorama.Fore.CYAN),
                               client=client)

    all_channels = [\
                    channel_stdout,
                    channel_messages_ngmg,
                    channel_messages_solaris,
                    channel_ep,
                    channel_mslogfmt,
                    #channel_dcisnoop,
                    #channel_apitrace,
                    ]
    # -------------------------------------------------------------------------

    for channel in all_channels:
        channel.initialize()
    channel_objects = [channel.channel for channel in all_channels]

    try:
        while True:
            rl, wl, xl = select.select(channel_objects,[],[],1.0)
            if len(rl) > 0:
                for channel in all_channels:
                    channel_object = channel.channel
                    if channel_object in rl and channel_object.recv_ready():
                        raw_output = channel_object.recv(1024)
                        processed_output = strip_control_characters(raw_output.rstrip())
                        print channel.color + processed_output
    finally:
        for channel in channel_objects:
            channel.close()
        client.close()

if __name__ == "__main__":
    hostname = sys.argv[1]
    username = 'root'
    password = '!bootstrap'
    main(hostname, username, password)

