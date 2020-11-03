import logging
import os
import json

logging.basicConfig(filename='output.log', level=logging.CRITICAL)

class Analyzer:
    def __init__(self, file_path=None,):  
        self.file_path = file_path

    def __enter__(self):
        self.file = open(self.file_path, 'r')
        self.obj  = json.load(self.file)
        return self.obj

    def __exit__(self, type, value, traceback):
        self.file.close()
    
    