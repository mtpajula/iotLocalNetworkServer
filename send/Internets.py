# -*- coding: utf-8 -*-
import urllib.request
import json

class Internets:

    messages = {}

    def __init__(self, settings):
        self.s = settings
        self.devices = APIelement(self.s, "device")
        self.get_devices()

    def get_devices(self):
        self.messages.clear()
        dev_dict = self.devices.read_data()

        for d in dev_dict:
            m = APIelement(self.s, "message", d["id"])
            if "description" in d:
                m.description = d["description"]
            self.messages[d["title"]] = m

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
                    d.receive_command(c["title"], c["description"])

    def __str__(self):
        s = "\nInternets devices:\n"
        for key, value in self.messages.items():
            s += "\t" + key + "\t\t" + value.description + "\n"
        return s



class APIelement:

    parent_id   = ""
    description = ""

    def __init__(self, settings, c, parent = None):
        self.s = settings
        self.controller = c
        if parent != None:
            self.parent_id = parent

    def create_get_request(self, params):
        params['controller'] = self.controller
        params['app_id'] = self.s.internets()["app_id"]

        s = self.s.internets()["address"]
        for key, value in params.items():
            if value != "":
                s += key + "=" + value + "&"

        print(s)
        return s


    def create_data(self, title, description):
        print("inserting data")

        title = title.replace(" ", "%20")
        description = description.replace(" ", "%20")

        params = {
                'action'     : 'create',
                'parent_id'  : self.parent_id,
                'title'      : title,
                'description': description
            }

        self.call(params)

    def read_data(self):
        print("reading data")

        params = {
                'action'     : 'read',
                'parent_id'  : self.parent_id
            }

        return self.call(params)["data"]

    def call(self, params):

        url = self.create_get_request(params)

        try:
            req = urllib.request.Request(url)
            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))
            print(cont)
            return cont
        except Exception as e:
            print(str(e))
            return {}
