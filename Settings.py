# -*- coding: utf-8 -*-
import json
import os

class Settings:

    data = {}

    def for_collector(self):
        return self.data["collector"]

    def for_internets(self):
        return self.data["internets"]

    def load(self, filepath):

        filepath = os.getcwd() + "/" + filepath

        print ("Loading settings from:")
        print(filepath)

        try:
            with open(filepath) as f:
                self.data = json.load(f)
        except Exception as e:
            print(str(e))
