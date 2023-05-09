#!/usr/bin/env python3
'''
 # @ Project: fileget.py
 # @ NAME: IPK Project 1
 # @ Author: Daniel Fajmon <xfajmo05@vutbr.cz>
 # @ Create Time: 28-03-2021 20:05:06
 # @ Description: Project for downloading files.
'''

import sys
import socket
import argparse
import re
from urllib.parse import urlparse
import os

# timeout in seconds
Timeout = 30
# bytes to recieve
Maxsize = 2048

# parse arguments 
parser = argparse.ArgumentParser()
parser.add_argument('-n', required=True, help="ip")
parser.add_argument('-f', required=True, help="file path")
args = parser.parse_args()

#check for ip address
if not ":" in args.n:
    sys.exit("Error ip address")

ip = re.split(":", args.n)
host = ip[0]
port = int(ip[1])
surl = urlparse(args.f)
filepath = surl.path[1:]

# setup message
msgUDP = f"WHEREIS {surl.netloc}"

# check for fsp://
if not re.search("^[fF][sS][pP]:\/\/[a-zA-Z0-9.-\_]+\/.*$", args.f):
    sys.exit("Error, not valid SURL")

#WHEREIS
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
    try:
        udp.settimeout(Timeout)
        udp.sendto(bytes(msgUDP, "utf-8"), (host, port))
        recvMsg = udp.recvfrom(Maxsize)
        addressTCP = recvMsg[0].decode()

        if(addressTCP == "ERR Not Found"):
            sys.exit("Error not found")

        if(addressTCP == "ERR Syntax"):
            sys.exit("Syntax error")

    except socket.timeout:
        udp.close()
        sys.exit("Timeout exception")

#split ip to host and port
ipTCP = re.split(":|, |\s", addressTCP)
host = ipTCP[1]
port = int(ipTCP[2])

#GET file
def getFile(filepath, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        try:
            tcp.settimeout(Timeout)
            tcp.connect((host, port))
            tcp.send(bytes(f"GET {filepath} FSP/1.0\r\n Hostname: {surl.netloc}\r\n Agent: xfajmo05\r\n\r\n", "utf-8"))
            recvMsg = tcp.recv(Maxsize)
            header,data = recvMsg.split(b"\r\n\r\n",1)

            if not b"Success" in header:
                sys.exit("File error")

            file = open(os.path.split(filepath)[1], "wb")
            file.write(data)

            while True:
                data = tcp.recv(Maxsize)
                if data == b"" or not data:
                    break
                file.write(data)

            file.close()
            tcp.close()

        except socket.timeout:
            tcp.close()
            sys.exit("ERROR: Server timeout")

if (filepath == "*"):
    getFile("index", host, port)
    with open('index') as f:
        for line in f:
            line = line.strip("\r\n")
            if line != "":
                getFile(line, host, port)
else:
    getFile(filepath, host, port)