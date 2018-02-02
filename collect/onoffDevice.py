# -*- coding: utf-8 -*-
from .Device import *

class onoffDevice(Device):

    switch = False

    def __init__(self, ip, root):
        super().__init__(ip, root)
        self.type = "onoffDevice"

    def set(self, sw):
        self.switch = sw
        s = self.call(self.switch_str())
        self.get_state(s)

    def get_state(self, s = None):
        if s == None:
            s = self.get_status()

        if s["status"] == "off":
            self.switch = False
        elif s["status"] == "on":
            self.switch = True

    def switch_str(self):
        if self.switch:
            return "on"
        return "off"

    def receive_command(self, category, command):

        if command == "off":
            self.set(False)
        elif command == "on":
            self.set(True)
        elif command == "status":
            self.get_state()
            self.send_message("device status", self.switch_str())
        elif command == "info":
            self.send_message("device info", self.__str__())
        else:
            super(onoffDevice, self).receive_command(category, command)

    def  __str__(self):
        s = super(onoffDevice, self).__str__()
        return s + " Status: " + self.switch_str()
