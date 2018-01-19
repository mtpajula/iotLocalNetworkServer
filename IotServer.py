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

    def  __str__(self):
        s = "\nServer:\n\t" + super(IotServerDevice, self).__str__()
        return s + "\n"


class IotServer:

    s = Settings()

    def __init__(self):
        self.d = IotServerDevice()
        self.s.load("data/settings.json")
        self.c = Collector(self.s.for_collector())
        self.i = Internets(self.s.for_internets())
        print(self.i)

    def collect_data(self):
        self.c.start()
        print(self.c)
        print(self.d)

    def send_internets(self):
        devices = self.c.devices
        devices.append(self.d)
        self.i.send(devices)

    def get_internets(self):
        devices = self.c.devices
        devices.append(self.d)
        self.i.get(devices)


print("-- IotServer --")
iot = IotServer()
iot.collect_data()
#iot.d.send_message("testi","from server")
#iot.send_internets()
iot.get_internets()
iot.send_internets()


# TODO filter internets commands
# TODO save Collector result
# TODO fix stuck Collector when testing ips

#iot.send_data("testdata")
#iot.get_commands_from_internets()

print("-- end --")
