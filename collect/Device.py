# -*- coding: utf-8 -*-
import urllib.request
import json

class Device:

    ip       = "---"
    name     = ""
    task     = ""
    type     = "none"
    timeo    = 8

    def __init__(self):
        self.messages = []

    def add_root_data(self, ip, root = None):
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
        self.send_message("command not found", command)

    def send_message(self, title, desc):
        self.messages.append({"title":title,"desc":desc})
        #self.messages[title] = desc
