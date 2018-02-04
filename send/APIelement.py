# -*- coding: utf-8 -*-
import urllib.request
import json

class APIelement:

    parent_id   = ""
    description = ""

    def __init__(self, settings, c, parent = None):
        self.s = settings
        self.controller = c
        if parent != None:
            self.parent_id = parent

    def __str__(self):
        s = self.controller + ": "
        s += self.parent_id
        return s

    def create_get_request(self, params):
        params['controller'] = self.controller
        params['app_id'] = self.s.internets()["app_id"]

        s = self.s.internets()["address"]
        for key, value in params.items():
            if value != "":
                s += key + "=" + value + "&"

        #print(s)
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

    def delete_data(self, id):
        print("deleting data")

        params = {
                'action'     : 'delete',
                'parent_id'  : self.parent_id,
                'id'      : id
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
        print(url)

        try:
            req = urllib.request.Request(url)
            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))
            #print(cont)
            return cont
        except Exception as e:
            print(str(e))
            return {}
