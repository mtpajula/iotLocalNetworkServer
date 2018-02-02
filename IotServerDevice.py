# -*- coding: utf-8 -*-
from collect.Collector import Collector
from collect.Device import *
from send.Internets import Internets
from Settings import Settings

class IotServerDevice(Device):

    def __init__(self):
        super().__init__("noip")
        self.type = "IOTLocalServer"
        self.name = "server"
        self.task = "server"

        self.s    = Settings()
        self.s.load("data/settings.json")
        self.c    = Collector(self.s)
        self.i    = Internets(self.s)

    def  __str__(self):
        s = "Server:\n\t" + super(IotServerDevice, self).__str__()
        return s + "\n"

    def collect_iot(self, load=False):
        if load:
            self.c.load()
        else:
            self.c.start()
        print(self.c)
        print(self)

    def receive_command(self, category, command):

        if command == "reset devices":
            self.i.get_devices()
            self.collect_iot()
            self.send_message("internet device reset", "devices: " + str(len(self.i.messages)))
            self.send_message("iot device reset", "devices: " + str(len(self.c.devices)+1))
        else:
            super(IotServerDevice, self).receive_command(category, command)
