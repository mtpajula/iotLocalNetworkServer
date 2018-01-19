# -*- coding: utf-8 -*-
import nmap
from .Device import *

class Collector:

    devices = []

    def __init__(self, settings):
        self.s = settings

    def start(self):
        ips = self.get_ip_list()
        self.find_iot_devices(ips)

    def get_ip_list(self):
        print("Collecting iot data")
        nm = nmap.PortScanner()
        nm.scan(self.s["ip_range"], arguments="-sP")
        print(nm.all_hosts())
        return nm.all_hosts()

    def find_iot_devices(self, ips):

        self.devices.clear()

        for ip in ips:
            d = Device(ip)
            print("checking ip: " + ip)
            out = d.call("")
            if "device" in out:
                print(" == device found == ")
                self.create_device(ip, out)
            else:
                print("ip not valid iot device")

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
