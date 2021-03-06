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
    
### Setting up

 1. cp data/settings.demo.json data/settings.json
 2. Open data/settings.json
 3. settings.json: insert your MySQL-login -information
 4. settings.json: Change nmap ip-range settings if needed

## Running

    python3 IotServer.py                                      # Normal mode
    python3 IotServer.py status                               # status mode
    python3 IotServer.py schedule                             # Schedule mode
    python3 IotServer.py device=server command"reset devices" # Command mode
    
 * Normal mode runs commands and sends messages (php-api can run)
 * Status mode saves device statuses to db and sends messages (ex. cron every hour)
 * Schedule mode runs schedules, commands and saves messages (ex. cron every minute)

## About python-nmap

nmap command and its equivalent in python-nmap:

    nmap -sP 192.168.1.100-200
    nm.scan("192.168.1.100-200", arguments="-sP")

