# -*- coding: utf-8 -*-
import urllib.request
import json
import nmap
from .Device import *
from .onoffDevice import *

class Collector:

    devices  = []
    filepath = "data/collector.json"
    timeo    = 8
    virtual  = "/virtualdevs"

    def __init__(self, settings):
        self.s = settings

    def start(self):
        ips = self.get_ip_list()
        self.find_iot_devices(ips)

    def load(self):
        self.devices.clear()

        if not self.s.is_file(self.filepath):
            print("No saved collector data")
            self.start()
            return

        data = self.s.read(self.filepath)

        for d in data:
            self.create_device(d["ip"], d["root"])

    def save(self):
        data = []
        for d in self.devices:
            data.append(d.get_dict())

        self.s.write(self.filepath, data)

    def get_ip_list(self):
        print("Collecting iot data")
        nm = nmap.PortScanner()
        nm.scan(self.s.collector()["ip_range"], arguments="-sP")
        print(nm.all_hosts())
        return nm.all_hosts()

    def request_json(self, addr):
        url = "http://" + addr
        print("requesting json from " + url)

        try:
            req = urllib.request.Request(url)
            r = urllib.request.urlopen(req, timeout = self.timeo).read()
        except Exception as e:
            return False, "urllib"

        try:
            out = json.loads(r.decode('utf-8'))
            return True, out
            #print(out)
            if "device" in out:
                print(" == device found == ")
                return True, out
        except Exception as e:
            return False, "json"

    def find_virtual_iot_devices(self, addr):
        vurl = addr + self.virtual;
        status, out = self.request_json(vurl)
        if status:
            if "devices" in out:
                print(" == virtual iot server found == ")
                for dev in out["devices"]:
                    self.find_iot_device(vurl + "/" + dev)
        else:
            print(out)

    def find_iot_device(self, addr):
        status, out = self.request_json(addr)

        if status:
            if "device" in out:
                print(" == device found == ")
                self.create_device(addr, out)
        else:
            if out == "json":
                self.find_virtual_iot_devices(addr)

    def find_iot_devices(self, ips):
        self.devices.clear()

        for ip in ips:
            self.find_iot_device(ip)

        self.save()

    def create_device(self, ip, root):
        if root["task"] == "onoff":
            self.devices.append(onoffDevice(ip, root))
        else:
            self.devices.append(Device(ip, root))

    def __str__(self):
        s = "\nCollector devices:\n"
        for d in self.devices:
            s += "\t" + d.__str__() + "\n"
        return s

    def send_command(self, name, command):
        for d in self.devices:
            if d.name == name:
                d.receive_command(command)
