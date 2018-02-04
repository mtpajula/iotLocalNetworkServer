# -*- coding: utf-8 -*-
from IotServerDevice import *
from time import sleep
import copy

class IotServer:

    wait = 10

    def __init__(self):
        print("\nIotServer init\n")
        self.d = IotServerDevice()

    def load_data(self):
        self.d.collect_iot(True)

    def collect_data(self):
        self.d.collect_iot()

    def send_internets(self):
        #devices =  copy.copy(self.d.c.devices)
        #devices =  copy.deepcopy(self.d.c.devices)
        #devices.append(self.d)
        #self.d.i.send(devices)
        self.d.i.send(self.d.c.devices)
        self.d.i.send([self.d])

    def get_internets(self):
        #devices = copy.copy(self.d.c.devices)
        #devices.append(self.d)
        self.d.i.get(self.d.c.devices)
        self.d.i.get([self.d])

    def loop(self):
        # TODO if new commands, loop faster
        # TODO better print
        # example: commands per dev?
        # TODO collect devices once a day or in case of commands
        # TODO Fix mess that was left behind after fixing inheritancebug
        # (all devices shared messages-list)

        self.d.i.get_devices()
        self.load_data()

        while True:
            print("\nsleep\n")
            sleep(self.wait)
            self.run()

    def run(self):
        self.get_internets()
        self.send_internets()
        # TODO filter internets commands


if __name__ == '__main__':
    print("-- IotServer --")
    iot = IotServer()
    iot.loop()
