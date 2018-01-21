# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

class Settings:

    data = {}

    def collector(self):
        return self.data["collector"]

    def internets(self):
        return self.data["internets"]

    def is_file(self, filepath):
        filepath = os.getcwd() + "/" + filepath
        f = Path(filepath)

        if f.is_file():
            return True
        return False


    def load(self, filepath):
        self.data = self.read(filepath)

    def read(self, filepath):
        filepath = os.getcwd() + "/" + filepath

        print ("Reading from: " + filepath)

        out = {}

        try:
            with open(filepath) as f:
                out = json.load(f)
        except Exception as e:
            print(str(e))

        return out

    def write(self, filepath, data):
        filepath = os.getcwd() + "/" + filepath

        print ("Writing to: " + filepath)

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(str(e))
