# -*- coding: utf-8 -*-
import urllib.request
import json

class Internets:

    controller        = "message"

    def __init__(self, settings):
        self.s = settings

    def create_get_request(self, params):
        params['controller'] = self.controller
        params['app_id'] = self.s["app_id"]

        s = self.s["address"]
        for key, value in params.items():
            s += key + "=" + value + "&"

        print(s)
        return s


    def create_data(self, title, description):
        print("inserting data")

        params = {
                'action'     : 'create',
                'parent_id'  : self.s["server_output_id"],
                'title'      : title,
                'description': description
            }

        self.call(params)

    def read_data(self):
        print("reading data")

        params = {
                'action'     : 'read',
                'parent_id'  : self.s["server_input_id"]
            }

        self.call(params)

    def call(self, params):

        url = self.create_get_request(params)

        try:
            req = urllib.request.Request(url)
            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))
            print(cont)
        except Exception as e:
            print(str(e))
