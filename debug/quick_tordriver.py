#!/usr/local/opt/python3/bin/python3

from bencoding.bencode import encode, decode
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
ALPHANUM = ascii_letters + digits
peer_id = ('-st0001' + ''.join(random.sample(ALPHANUM, 13)))



def get_peer_list(torrent_path):
    # Open torrent and read data into data variable
    data = None
    with open(torrent_path, 'rb') as f:
        read_data = f.read()
        data = decode(read_data)
    # pp.pprint(data)

    # Generate hash of info field
    info_hash = hashlib.sha1(encode(data[b'info'])).digest()
    
    # Calculate length of all torrent files, assume these are all multi-torrent files
    length = 0
    for file in data[b'info'][b'files']:
        length += file[b'length']

    # Make requests to a bunch of trackers and get the list of peers
    decoded_peers = []
    for tracker_list in data[b'announce-list']:
        for tracker in tracker_list:
            if(tracker.decode("utf-8")[:3] == "udp"):
                # print("udp tracker not supported")
                decoded_peers = request_peers_http("http" + tracker.decode("utf-8")[3:], info_hash, length)
            elif(tracker.decode("utf-8")[:4] == "http"):
                decoded_peers = request_peers_http(tracker.decode("utf-8"), info_hash, length)
            else:
                print("skipping - Unknown tracker url format: " + tracker[0])
    return(decoded_peers)

# This chunk of code was written because adam is a shoot first ask questions later type of person
'''
def request_peers_udp(tracker, info_hash, length):
    payload = {'info_hash': info_hash, 'peer_id': peer_id, 'length': length,
               'port': 6881, 'uploaded':0, 'downloaded':0, 'compact':1}

    tracker_hostname = urlparse(tracker).hostname
    tracker_port = urlparse(tracker).port
    tracker_path = urlparse(tracker).path

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    try:
        conn = (socket.gethostbyname(tracker_hostname), tracker_port)
    except:
        return # skip trackers we can't get the ip of

    print('preparing udp request for: ' + tracker)

    # obtain a connection ID by sending a connection request, this is where communication starts
    connection_id = 0x41727101980 #default connection id
    action = 0x0 #action (0 = give me a new connection id)  
    transaction_id = int(random.randrange(0, 255)) # get random transaction id
    connection_request = struct.pack("!q", connection_id) #first 8 bytes is connection id
    connection_request += struct.pack("!i", action) #next 4 bytes is action
    connection_request += struct.pack("!i", transaction_id) #next 4 bytes is transaction id
    connection_request += struct.pack("!i", 0x0) #padding so we send 16 bytes
    print(connection_request)
    sock.sendto(connection_request, conn)
    try:
        response = sock.recvfrom(2048)[0]
        print(response)
    except Exception as e:
        print(e)
        return

    # parse response to make sure it is valid and contains a connection_id
    if len(response) < 16:
        raise RuntimeError("Wrong response length getting connection id: %s" % len(response))            
    action = struct.unpack_from("!i", response)[0] #first 4 bytes is action
    res_transaction_id = struct.unpack_from("!i", response, 4)[0] #next 4 bytes is transaction id
    if res_transaction_id != transaction_id:
        raise RuntimeError("Transaction ID doesnt match in connection response! Expected %s, got %s"
            % (transaction_id, res_transaction_id))
    if action == 0x0:
        connection_id = struct.unpack_from("!q", response, 8)[0] #unpack 8 bytes from byte 8, should be the connection_id
    print('got connection id ' + str(connection_id))

    # send announce request
    action = 0x2 #action (2 = scrape)
    transaction_id = int(random.randrange(0, 255)) # get new random transaction id
    announce_request = struct.pack("!q", connection_id) #f irst 8 bytes is connection id
    announce_request += struct.pack("!i", action) # next 4 bytes is action
    announce_request += struct.pack("!i", transaction_id) # followed by 4 byte transaction id
    announce_request += struct.pack("!20s", info_hash)
    announce_request += struct.pack("!20s", bytearray(peer_id, 'utf8'))
    announce_request += struct.pack("!q", 0x0) # amount downloaded
    announce_request += struct.pack("!q", length) # amount left
    announce_request += struct.pack("!q", 0x0) # amount uploaded
    announce_request += struct.pack("!i", 0x0) # event 0 // 0: none; 1: completed; 2: started; 3: stopped
    announce_request += struct.pack("!i", 0x0) # IP address      0 // default
    announce_request += struct.pack("!i", 0x0) # key, not sure what this is for will try setting it to 0 and see if that works :)
    announce_request += struct.pack("!i", -1) # num_want -1 // default
    announce_request += struct.pack("!h", 6881) # port
    announce_request += struct.pack("!h", 0x0) # 2 bytes padding
    print(announce_request)
    sock.sendto(announce_request, conn)

    # parse announce request
    try:
        response = sock.recvfrom(2048)[0]
        # action = struct.unpack_from("!i", response)[0] # 
        transaction_id = struct.unpack_from("!i", response, 4)[0] # 
        # interval = struct.unpack_from("!i", response, 8)[0] # 
        # leechers = struct.unpack_from("!i", response, 16)[0] # 
        # seeders = struct.unpack_from("!i", response, 20)[0] # 
        # print(action, transaction_id, interval, leechers, seeders)
        print(response)
    except Exception as e:
        print(e)
        return

    # send scrape request
    action = 0x2 # action (2 = scrape)  
    transaction_id = int(random.randrange(0, 255)) # get random transaction id
    scrape_request = struct.pack("!q", connection_id) #first 8 bytes is connection id
    scrape_request += struct.pack("!i", action) #next 4 bytes is action
    scrape_request += struct.pack("!i", transaction_id) #next 4 bytes is transaction id
    scrape_request += struct.pack("!20s", info_hash)
    print('sending scrape request...')
    print(scrape_request)
    sock.sendto(scrape_request, conn)
    try:
        response = sock.recvfrom(2048)[0]
        print(response)
    except Exception as e:
        print(e)
        return

    sock.close()
    return
'''

def request_peers_http(tracker, info_hash, length):
    decoded_peers = []
    payload = {'info_hash': info_hash, 'peer_id': peer_id, 'length': length, 'uploaded':0, 'downloaded':0, 'compact':1}
    try:
        print('Attempting connection to: ' + tracker)
        r = requests.get(tracker, params=payload, timeout=3, verify=False)
        if(r.status_code == 200):
            # Grab the peers and split them into manageable chunks
            peers = decode(r.content)[b'peers']
            peers = [peers[i:i+6] for i in range(0, len(peers), 6)]
            # For each peer: print the ip and unpack the last 2 bytes as an int for the port
            for p in peers:
                ip = str(socket.inet_ntoa(p[:4]))
                port = str(unpack(">H", p[4:])[0])
                decoded_peers.append((ip, port))
    except Exception as e:
        print('Error connecting to: ' + tracker)
        pass
    return(decoded_peers)

for file in os.listdir('sample_torrents'):
    print('\n========================================================================================')
    print('getting list of peers for ' + file)
    peers = get_peer_list('sample_torrents/' + file)
    print('got the following peers: ')
    pp.pprint(peers)
    print('========================================================================================')