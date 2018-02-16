# -*- coding: utf-8 -*-

class DbObject:

    def __init__(self):
        self.id      = ""
        self.device  = ""
        self.payload = ""
        self.time    = ""
        self.address = ""
        self.name    = ""
        self.task    = ""
        self.start   = ""

    def __str__(self):
        s = str(self.id)  + " "
        s += self.device  + " "
        s += self.payload + " "
        s += self.time.strftime("%Y-%m-%d %H:%M:%S") + " "
        s += self.address + " "
        s += self.name    + " "
        s += self.task    + " "
        s += self.start
        return s
