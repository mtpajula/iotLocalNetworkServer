# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

class Settings:

    data      = {}
    directory =  os.path.abspath(os.path.dirname(__file__))

    def collector(self):
        return self.data["collector"]

    def internets(self):
        return self.data["internets"]

    def is_file(self, filepath):
        filepath = self.directory + "/" + filepath
        f = Path(filepath)

        if f.is_file():
            return True
        return False


    def load(self, filepath):
        self.data = self.read(filepath)

    def read(self, filepath):
        filepath = self.directory + "/" + filepath

        print ("Reading from: " + filepath)

        out = {}

        try:
            with open(filepath) as f:
                out = json.load(f)
        except Exception as e:
            print(str(e))

        return out

    def write(self, filepath, data):
        filepath = self.directory + "/" + filepath

        print ("Writing to: " + filepath)

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(str(e))
