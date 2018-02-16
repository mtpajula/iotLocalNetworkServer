# -*- coding: utf-8 -*-
from collect.Collector import Collector
from db.Connector import Connector
from collect.Device import *
from Settings import Settings

class IotServerDevice(Device):

    def __init__(self):
        super().__init__()
        self.type = "IOTLocalServer"
        self.name = "server"
        self.task = "server"

        self.s    = Settings()
        self.s.load("data/settings.json")
        self.c    = Collector(self.s)
        self.db   = Connector(self.s)

    def  __str__(self):
        s = "Server:\n\t" + super(IotServerDevice, self).__str__()
        return s + "\n"

    def get_status(self):
        return {"status":"ok"}

    def collect_iot(self, load = False):
        if load:
            print("\n")
            print("Load devices from db")
            print("======================================")
            devs = self.db.get_devices()
            self.c.put(devs)
            print(self.c)
            print(self)
        else:
            print("\n")
            print("Search devices from network")
            print("======================================")
            self.c.start()
            print(self.c)
            print(self)
            print("Save devices to db")
            self.db.set_devices(self.c.devices)



    def receive_command(self, category, command):

        if command == "reset devices":
            self.collect_iot()
            self.send_message("iot device reset", "devices: " + str(len(self.c.devices)+1))
        else:
            super(IotServerDevice, self).receive_command(category, command)
