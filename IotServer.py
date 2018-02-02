# -*- coding: utf-8 -*-
from collect.Collector import Collector
from collect.Device import *
from send.Internets import Internets
from Settings import Settings
from time import sleep

class IotServerDevice(Device):

    def __init__(self, collector):
        super().__init__("noip")
        self.type = "IOTLocalServer"
        self.name = "server"
        self.task = "server"
        self.c    = collector

    def  __str__(self):
        s = "\nServer:\n\t" + super(IotServerDevice, self).__str__()
        return s + "\n"


class IotServer:

    s    = Settings()
    wait = 10

    def __init__(self):
        self.s.load("data/settings.json")
        self.c = Collector(self.s)
        self.i = Internets(self.s)

        self.d = IotServerDevice(self.c)
        print(self.i)

    def collect_data(self):
        self.c.start()
        #self.c.load()
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

    def loop(self):
        # TODO if new commands, loop faster
        # TODO better print
        # example: commands per dev?
        # TODO collect devices once a day or in case of commands
        while True:
            sleep(self.wait)
            self.run()

    def run(self):
        print("-- IotServer --")
        #self.collect_data()
        #iot.d.send_message("testi","from server")
        #iot.send_internets()
        self.get_internets()
        self.send_internets()

        # TODO filter internets commands

        #iot.send_data("testdata")
        #iot.get_commands_from_internets()
        print("-- end --")

if __name__ == '__main__':
    print("-- IotServer --")
    iot = IotServer()
    iot.loop()
