# -*- coding: utf-8 -*-
import sqlite3
from .DbObject import *

class DbConnection:

    def __init__(self, settings):
        self.s    = settings
        self.conn = sqlite3.connect(self.s.connector()["sqlite3"])

    def get(self, table, id = None):
        sql = ''
        if id == None:
            sql = 'SELECT * FROM ' + table
        else:
            sql = 'SELECT * FROM ' + table + ' WHERE id = ' + str(id)

        rows = self.runSql(sql)

        dbos = []
        for r in rows:
            dbo = DbObject();
            dbo.id     = r[0]
            if table in "command message status":
                dbo.device  = r[1]
                dbo.payload = r[2]
                dbo.time    = r[3]
            elif table in "schedule":
                dbo.device  = r[1]
                dbo.start   = r[2]
                dbo.payload = r[3]
                dbo.time    = r[4]
            elif table in "device":
                dbo.address = r[1]
                dbo.name    = r[2]
                dbo.task    = r[3]
                dbo.time    = r[4]
            dbos.append(dbo)

        return dbos

    def runSql(self, sql):
        #print(sql)
        c = self.conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        self.conn.commit()
        c.close()
        #self.conn.close()
        return rows

    def getDbo(self):
        return DbObject();

    def put(self, table, dbo):
        #print(dbo)
        sql = ""
        if table in "command message status":
            sql += "UPDATE "+table+" SET"
            sql += " device='"+dbo.device+"', payload='"+dbo.payload+"'"
            sql += " WHERE id="+str(dbo.id)
        elif table in "schedule":
            sql += "UPDATE "+table+" SET"
            sql += " device='"+dbo.device+"', start='"+dbo.start+"', payload='"+dbo.payload+"'"
            sql += " WHERE id="+str(dbo.id)
        elif table in "device":
            sql += "UPDATE "+table+" SET"
            sql += " address='"+dbo.address+"', name='"+dbo.name+"', task='"+dbo.task+"'"
            sql += " WHERE id="+str(dbo.id)

        return self.runSql(sql)

    def post(self, table, dbo):
        #print(dbo)
        sql = ""
        if table in "command message status":
            sql += "INSERT INTO "+table
            sql += " (device, payload)"
            sql += " VALUES ('"+dbo.device+"', '"+dbo.payload+"')"
        elif table in "schedule":
            sql += "INSERT INTO "+table
            sql += " (device, start, payload)"
            sql += " VALUES ('"+dbo.device+"', '"+dbo.start+"', '"+dbo.payload+"')"
        elif table in "device":
            sql += "INSERT INTO "+table
            sql += " (address, name, task)"
            sql += " VALUES ('"+dbo.address+"', '"+dbo.name+"', '"+dbo.task+"')"

        return self.runSql(sql)

    def delete(self, table, dbo):
        #print(dbo)
        sql = "DELETE FROM " + table
        sql += " WHERE id = "+ str(dbo.id)
        return self.runSql(sql)

    def clear(self, table):
        sql = "DELETE FROM " + table
        return self.runSql(sql)
