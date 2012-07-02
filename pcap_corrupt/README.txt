NOTE:

You must patch scapy to be able to build RTP packets.

Go to /usr/local/lib/python2.7/site-packages/scapy/layers/rtp.py, modify
line 31, i.e. the "BitEnumField" for the RTP payload, and change the variable
name from:

'payload'

to:

'rtp_payload'

else you hit a recursion error while executing do_build() because 'payload'
is a special variable.
