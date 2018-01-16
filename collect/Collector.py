# -*- coding: utf-8 -*-
import nmap

class Collector:

    def __init__(self, settings):
        self.s = settings

    def start(self):
        ips = get_ip_list()

    def get_ip_list(self):
        print("Collecting iot data")
        nm = nmap.PortScanner()
        nm.scan(self.s["ip_range"], arguments="-sP")
        print(nm.all_hosts())
        return nm.all_hosts()
