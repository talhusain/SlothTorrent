#!/usr/local/opt/python3/bin/python3

# Requirements: bencoder & requests
#   - can be gotten via 'pip install bencoder requests'
from bencoding.bencode import encode, decode
import urllib
import hashlib
import requests
import socket
import random
import os
from struct import unpack
from string import ascii_letters, digits


import pprint
pp = pprint.PrettyPrinter(indent=2)

# GLOBALS:
torrent_path = '/Users/afurbee/Downloads/X-Men- Apocalypse (2016) [1080p] [YTS.AG].torrent'



def get_peer_list(torrent_path):
    # Open torrent and read data into data variable
    data = None
    with open(torrent_path, 'rb') as f:
        read_data = f.read()
        data = decode(read_data)

    # Generate hash of info field
    info_hash = hashlib.sha1(encode(data[b'info'])).digest()
    
    # Generate static peer_id, just for PoC
    VERSION = '0001'
    ALPHANUM = ascii_letters + digits
    peer_id = ('-DR' + VERSION + ''.join(random.sample(ALPHANUM, 13)))
    
    # Calculate length of all torrent files, assume these are all multi-torrent files
    length = 0
    for file in data[b'info'][b'files']:
        length += file[b'length']

    # Make requests to a bunch of trackers and get the list of peers
    decoded_peers = []
    for tracker in data[b'announce-list']:
        payload = {'info_hash': info_hash, 'peer_id': peer_id, 'length': length,
                    'port': 6881, 'uploaded':0, 'downloaded':0, 'compact':1}
        try:
            print('Attempting connection to:')
            print('http://' + tracker[0].decode("utf-8")[6:])
            r = requests.get('http://' + tracker[0].decode("utf-8")[6:], params=payload, timeout=3)
            if(r.status_code == 200):
                # print('http://' + tracker[0].decode("utf-8")[6:])
                # Grab the peers and split them into manageable chunks
                peers = decode(r.content)[b'peers']
                peers = [peers[i:i+6] for i in range(0, len(peers), 6)]
                # For each peer: print the ip and unpack the last 2 bytes as an int for the port
                for p in peers:
                    ip = str(socket.inet_ntoa(p[:4]))
                    port = str(unpack(">H", p[4:])[0])
                    decoded_peers.append((ip, port))
        except Exception as e:
            print(e)
            pass
    pp.pprint(decoded_peers)
    return(decoded_peers)

for file in os.listdir('sample_torrents'):
    print('getting list of peers for ' + file)
    get_peer_list(torrent_path)
    print('========================================================================================')