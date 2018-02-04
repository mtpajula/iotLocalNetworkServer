# iotLocalNetworkServer

Local network server code to controll iot-devices and communicate with cloud api. Searches devices from local network, reads commands and sends messages to/from cloud api.

Prerequisites:

 * python3
 * nmap

Install:

    sudo apt install python3-pip
    sudo apt install nmap
    pip3 install python-nmap

Running:

    python3 IotServer.py

## About python-nmap

nmap command and its equivalent in python-nmap:

    nmap -sP 192.168.1.100-200
    nm.scan("192.168.1.100-200", arguments="-sP")
