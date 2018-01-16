# -*- coding: utf-8 -*-
import urllib.request
import json

class Device:

    name   = ""
    task   = ""
    type   = "none"

    def __init__(self, ip, root = None):
        self.ip = ip
        if root != None:
            self.name = root["device"]
            self.task = root["task"]

    def get_status(self):
        return self.call("status")

    def call(self, params):

        url = "http://" + self.ip + "/" + params
        print(url)

        try:
            req = urllib.request.Request(url)
            r = urllib.request.urlopen(req).read()
            m = json.loads(r.decode('utf-8'))
            print(m)
            return m
        except Exception as e:
            print(str(e))

        return {}

    def __str__(self):
        s = " [" + self.ip + "] "
        s += ": " + self.name
        s += " (" + self.type + ")"
        return s

    def receive_command(self, command):
        return


class onoffDevice(Device):

    switch = False

    def __init__(self, ip, root):
        super().__init__(ip)
        self.type = "onoffDevice"
        self.name = root["device"]
        self.task = root["task"]

    def get_state(self):
        s = self.get_status()

        if s["status"] == "off":
            self.switch = False
        elif s["status"] == "on":
            self.switch = True

    def switch_str(self):
        if self.switch:
            return "on"
        return "off"

    def receive_command(self, command):
        if command == "off":
            print("TODO")
        elif command == "on":
            print("TODO")
        elif command == "status":
            print("TODO")

    def  __str__(self):
        s = super(onoffDevice, self).__str__()
        return s + " Status: " + self.switch_str()
