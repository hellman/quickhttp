#!/usr/bin/env python
#-*- coding:utf-8 -*-

class UploadFile:
    def __init__(self, filename, s):
        if type(s) == str:
            self.data = str(s)
        elif type(s) == file:
            self.data = s.read()
        else:
            raise TypeError("Unknown type passed to UploadFile")

        self.upload_name = filename
        self.size = len(self.data)

    def seek(self, x):
        pass

    def read(self, l=None):
        return self.data