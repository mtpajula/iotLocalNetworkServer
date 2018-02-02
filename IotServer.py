# -*- coding: utf-8 -*-
from collect.Collector import Collector
from collect.Device import *
from send.Internets import Internets
from Settings import Settings
from time import sleep

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
        self.i.get_devices()

    def  __str__(self):
        s = "\nServer:\n\t" + super(IotServerDevice, self).__str__()
        return s

    def receive_command(self, category, command):

        if command == "reset devices":
            self.i.get_devices()
            #self.c.start()
            self.send_message("internet device reset", "devices: " + str(len(self.i.messages)))
            self.send_message("iot device reset", "devices: " + str(len(self.c.devices)))
        else:
            super(IotServerDevice, self).receive_command(category, command)


class IotServer:

    wait = 10

    def __init__(self):
        print("\nIotServer init\n")
        self.d = IotServerDevice()

    def collect_data(self):
        self.d.c.start()
        #self.c.load()
        print(self.d.c)
        print(self.d)

    def send_internets(self):
        devices = self.d.c.devices
        devices.append(self.d)
        self.d.i.send(devices)

    def get_internets(self):
        devices = self.d.c.devices
        devices.append(self.d)
        self.d.i.get(devices)

    def loop(self):
        # TODO if new commands, loop faster
        # TODO better print
        # example: commands per dev?
        # TODO collect devices once a day or in case of commands
        while True:
            sleep(self.wait)
            self.run()

    def run(self):
        print("\nRun\n")
        #self.collect_data()
        #iot.d.send_message("testi","from server")
        #iot.send_internets()
        self.get_internets()
        self.send_internets()

        # TODO filter internets commands

        #iot.send_data("testdata")
        #iot.get_commands_from_internets()

if __name__ == '__main__':
    print("-- IotServer --")
    iot = IotServer()
    iot.run()
