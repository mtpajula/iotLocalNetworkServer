# -*- coding: utf-8 -*-
from .DbObject import *
from .DbConnection import DbConnection
import time
import json

class Connector:

    def __init__(self, settings):
        self.s   = settings
        self.con = DbConnection(self.s)

    def get_devices(self):
        dbos = self.con.get('device')
        out = []
        for dbo in dbos:
            if dbo.task != "server":
                i = {
                        "ip"   : dbo.address,
                        "root" : {
                            "device" : dbo.name,
                            "task"   : dbo.task
                        }
                    }
                out.append(i)

        return out

    def set_devices(self, devs):
        self.con.clear('device')
        for d in devs:
            dbo  = DbObject()
            dbo.address = d.ip
            dbo.name    = d.name
            dbo.task    = d.task
            #print(dbo)
            self.con.post('device', dbo)

    def get_commands(self, devs):
        dbos = self.con.get('command')
        self.run_command(devs, dbos)

    def get_schedules(self, devs):
        dbos = self.con.get('schedule')
        self.run_command(devs, dbos, 'schedule')

    def run_command(self, devs, dbos, table = 'command'):
        for d in devs:
            for dbo in dbos:
                if dbo.start != "":
                    if int(dbo.start) > time.time():
                        continue

                if d.name == dbo.device:
                    print(dbo)
                    d.receive_command(table, dbo.payload)
                    self.con.delete(table, dbo)

    def set_messages(self, devs):
        for d in devs:
            for m in d.messages:
                dbo  = DbObject()
                dbo.device  = d.name
                if m["title"] != "":
                    dbo.payload = m["title"] + ": " + m["desc"]
                else:
                    dbo.payload = m["desc"]
                print(dbo)
                self.con.post('message', dbo)

    def set_status(self, devs):
        for d in devs:
            s = d.get_status()
            dbo  = DbObject()
            dbo.device  = d.name
            dbo.payload = out = json.dumps(s)
            print(dbo)
            self.con.post('status', dbo)
