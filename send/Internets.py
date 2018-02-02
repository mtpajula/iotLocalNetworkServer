# -*- coding: utf-8 -*-
from .APIelement import *

class Internets:

    messages = {}
    ccat     = "command"

    def __init__(self, settings):
        self.s = settings
        self.devices = APIelement(self.s, "device")

    def get_devices(self):
        self.messages.clear()
        dev_dict = self.devices.read_data()

        for d in dev_dict:
            m = APIelement(self.s, "message", d["id"])
            if "description" in d:
                m.description = d["description"]
            self.messages[d["title"]] = m

        print(self.__str__())

    def send(self, devices):
        print("sending messages")
        for d in devices:
            if d.name in self.messages:
                for m in d.messages:
                    print("SEND: " + m + ", " + d.messages[m])
                    self.messages[d.name].create_data(m, d.messages[m])
                d.messages.clear()

    def get(self, devices):
        print("get commands")
        for d in devices:
            if d.name in self.messages:
                data_dict = self.messages[d.name].read_data()
                for c in data_dict:
                    if c["title"] != self.ccat:
                        continue

                    d.receive_command(c["title"], c["description"])
                    self.messages[d.name].delete_data(c["id"])

    def __str__(self):
        s = "\nInternets devices:\n"
        for key, value in self.messages.items():
            s += "\t" + key + "\t\t" + value.description + "\n"
        return s
