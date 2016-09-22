#!/usr/local/opt/python3/bin/python3

# Requirements: bencoder & requests
#   - can be gotten via 'pip install bencoder requests'
from bencoder import encode, decode
import urllib
import hashlib
import requests

# GLOBALS:
torrent_path = 'B:/learning/SHSU/00_fall-2016/software-engineering/project/debug/res/torrent-files/[a4e]Paranoia_Agent_01-13.torrent'

# Open torrent and read data into data variable
data = None
with open(torrent_path, 'rb') as f:
    read_data = f.read()
    data = decode(read_data)

# Generate hash of info field
info_hash = hashlib.sha1(encode(data[b'info'])).digest()

# Generate static peer_id, just for PoC
peer_id = bytes(range(20))

# Calculate length of all torrent files, assume these are all multi-torrent files
length = 0

print('\n')
print('\tLength:')
for file in data[b'info'][b'files']:
    print('\t' + str(file[b'length']))
    length += file[b'length']

# Make requests to a bunch of trackers
if not b'nodes' in data:
    if (b'announce'):
        #print('\n' + str(data) + '\n')
        for item in data:
            if (item == b'info'):
                for sub in item:
                    print(sub)
            else:
                print(item)
    elif (b'announce-list'):
        for tracker in data[b'announce-list']:
            payload = {'info_hash': info_hash, 'peer_id': peer_id.decode("utf-8"), 'length': length,
                        'port': 6881, 'uploaded':0, 'downloaded':0, 'compact':1}
            try:
                print('\n' + 'http://' + tracker[0].decode("utf-8")[6:])
                r = requests.get('http://' + tracker[0].decode("utf-8")[6:], params=payload, timeout=3)
                print(r.url)
                print(r.content)
            except:
                pass
