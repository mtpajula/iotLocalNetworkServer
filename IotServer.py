# -*- coding: utf-8 -*-
from collect.Collector import Collector
from send.Internets import Internets
from Settings import Settings

class IotServer:

    s = Settings()

    def __init__(self):
        self.s.load("data/settings.json")
        self.c = Collector(self.s.for_collector())
        self.i = Internets(self.s.for_internets())

    def collect_data(self):
        self.c.start()

    def send_data(self, str1):
        self.i.create_data("Collector", str1)

    def get_commands_from_internets(self):
        self.i.read_data()


print("-- IotServer --")
iot = IotServer()
iot.collect_data()
# TODO send receive commands
#iot.send_data("testdata")
#iot.get_commands_from_internets()

print("-- end --")
