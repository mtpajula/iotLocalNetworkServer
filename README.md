# iotLocalNetworkServer

Local network server code to controll iot-devices. Searches devices from local network, reads commands and sends messages to/from database.

Prerequisites:

 * nmap
 * python3
 * python3-mysqldb
 * python3-nmap

## Install prerequisites

    sudo apt install python3-mysqldb
    sudo apt install nmap
    sudo apt install python3-nmap

## Running

    python3 IotServer.py                                      # Normal mode
    python3 IotServer.py schedule                             # Schedule mode
    python3 IotServer.py device=server command"reset devices" # Command mode

## About python-nmap

nmap command and its equivalent in python-nmap:

    nmap -sP 192.168.1.100-200
    nm.scan("192.168.1.100-200", arguments="-sP")

