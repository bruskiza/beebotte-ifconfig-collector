#!/usr/bin/env python

import os
import subprocess
import re
from beebotte import *


if 'BBT_API' in os.environ:
    _hostname = os.environ['BBT_API']
else:
    _hostname = 'api.beebotte.com'

if 'BBT_TOKEN' in os.environ:
    _token = os.environ['BBT_TOKEN']
else:
    print "No token specified. We cannot post to Beebotte without it. Please "\
          "set the BBT_TOKEN environment variable."
    sys.exit()

if 'BBT_CHANNEL' in os.environ:
    _channel = os.environ['BBT_CHANNEL']
else:
    print "No channel specified. We cannot post to Beebotte without it. Please "\
          "set the BBT_CHANNEL environment variable."
    sys.exit()

bbt = BBT(token=_token, hostname=_hostname)

s = subprocess.Popen("ifconfig ", shell=True,
	stdout=subprocess.PIPE).stdout.read()
file = open("reference.txt", "r")
for LINE in file.readlines():
    if "inet addr" in LINE:
		ip = re.match(r'.*inet addr:(.*)\s+Bcast',
		LINE.rstrip()).group(1)
    elif "RX packets" in LINE:
		rx_packets = re.match(r'.*RX packets:(.*)\s+errors',
		LINE.rstrip()).group(1)
    elif "TX packets" in LINE:
		tx_packets = re.match(r'.*TX packets:(.*)\s+errors',
		LINE.rstrip()).group(1)
    elif "RX bytes" in LINE:
		rx_bytes = re.match(r'.*RX bytes:(.*) \(.*\)\s+TX bytes',
		LINE.rstrip()).group(1)
		tx_bytes = re.match(r'.*TX bytes:(.*) \(',
		LINE.rstrip()).group(1)

netif = {
	"rx_bytes": int(rx_bytes),
	"tx_bytes": int(tx_bytes),
	"rx_packets": int(rx_packets),
	"tx_packets": int(tx_packets)}

bbt.writeBulk(_channel, [
    {"resource": "ip", "data": ip},
    {"resource": "netif", "data": netif},

])
