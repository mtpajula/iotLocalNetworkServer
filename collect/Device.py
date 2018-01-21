# -*- coding: utf-8 -*-
import urllib.request
import json

class Device:

    name     = ""
    task     = ""
    type     = "none"
    messages = {}
    timeo    = 8

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
            r = urllib.request.urlopen(req, timeout = self.timeo).read()
            m = json.loads(r.decode('utf-8'))
            print(m)
            return m
        except Exception as e:
            print(str(e))

        return {}

    def get_dict(self):
        d = {
                "ip"   : self.ip,
                "root" : {
                    "device" : self.name,
                    "task"   : self.task
                }
            }
        return d


    def __str__(self):
        s = " [" + self.ip + "] "
        s += ": " + self.name
        s += " (" + self.type + ")"
        return s

    def receive_command(self, category, command):
        print("receive_command to " + self.name + ": " + category + ", " + command + ". no command found")
        return

    def send_message(self, title, desc):
        self.messages[title] = desc


class onoffDevice(Device):

    switch = False

    def __init__(self, ip, root):
        super().__init__(ip, root)
        self.type = "onoffDevice"
        #self.name = root["device"]
        #self.task = root["task"]

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

        if category != "device":
            print("receive_command to " + self.name + ": " + category + ", " + command + ". no category found")
            return

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
