# -*- coding: utf-8 -*-
from IotServerDevice import *
from time import sleep
import copy
import sys

class IotServer:

    wait = 10

    def __init__(self):
        self.d = IotServerDevice()

    def printer(self, category, message):
        if category == "t1":
            print("\n")
            print(message)
            print("======================================")
        elif category == "t2":
            print("\n")
            print(message)
            print("--------------------------------------")
        elif category == "p":
            print(message)
        elif category == "error":
            print(" ! ERROR: " + message)

    '''
    run in terminal command mode
    Example: IotServer.py device=server command="reset devices"
    '''
    def send_command(self, device, command):
        self.printer("p","Run in terminal command mode")

        #self.printer("t1","Load devices from db")
        self.d.collect_iot(True)
        for d in self.d.c.devices:
            if d.name == device:
                d.receive_command('command', command)
        if self.d.name == device:
            self.d.receive_command('command', command)

        # Send messages to db
        self.send_message();

    def close_db(self):
        self.d.db.con.conn.close()

    def send_message(self):
        self.printer("t1","Send messages to db")
        self.d.db.set_messages(self.d.c.devices)
        self.d.db.set_messages([self.d])

    '''
    run in normal mode
    '''
    def run(self, schedule = False):
        self.printer("p","Run in normal mode")
        # Get devs from db
        #self.printer("t1","Load devices from db")
        self.d.collect_iot(True)

        # get commands
        self.printer("t1","Get commands")
        self.d.db.get_commands(self.d.c.devices)
        self.d.db.get_commands([self.d])

        # Send messages to db
        self.send_message();

    '''
    run in schedule mode
    '''
    def runSchedule(self):
        self.printer("p","Run in schedule mode")
        # Get devs from db
        #self.printer("t1","Load devices from db")
        self.d.collect_iot(True)

        # Get scheduled commands
        self.printer("t1","Get scheduled commands")
        self.d.db.get_schedules(self.d.c.devices)
        self.d.db.get_schedules([self.d])

        # get commands
        self.printer("t1","Get commands")
        self.d.db.get_commands(self.d.c.devices)
        self.d.db.get_commands([self.d])

        # Send messages to db
        self.send_message();

    '''
    run in status mode
    '''
    def runStatus(self):
        self.printer("p","Run in status mode")
        # Get devs from db
        #self.printer("t1","Load devices from db")
        self.d.collect_iot(True)

        # save statuses to db
        self.printer("t1","Save statuses to db")
        self.d.db.set_status(self.d.c.devices)
        self.d.db.set_status([self.d])

        # Send messages to db
        self.send_message();


if __name__ == '__main__':
    iot = IotServer()

    if "schedule" in sys.argv:
        iot.runSchedule()
        iot.close_db()
        sys.exit()

    if "status" in sys.argv:
        iot.runStatus()
        iot.close_db()
        sys.exit()

    c = None
    d = None
    for ar in sys.argv:
        if "command=" in ar:
            arp = ar.split("=")
            c = arp[1]
        elif "device=" in ar:
            arp = ar.split("=")
            d = arp[1]

    if c != None and d != None:
        iot.send_command(d,c)
        iot.close_db()
        sys.exit()

    iot.run()
    iot.close_db()
