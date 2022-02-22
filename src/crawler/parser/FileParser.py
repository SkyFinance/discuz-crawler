'''
Author: Yaaprogrammer
Date: 2022-02-09 17:21:52
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 19:12:56

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
import json

from crawler.parser.BaseParser import BaseParser


class FileParser(BaseParser):

    def __GetName(self):
        fileName = json.loads(self.html)['data']['file_name']
        return fileName

    def __GetSize(self):
        fileSize = json.loads(self.html)['data']['file_size']
        return fileSize

    def __GetReleaseDate(self):
        releaseDate = json.loads(self.html)['data']['file_time']
        return releaseDate

    def __IsAvailable(self):
        return json.loads(self.html)['msg'] == "ok"

    def __GetKey(self):
        return self.data["code"]

    def GetResult(self):
        if (self.__IsAvailable() is False):
            return {
                "key": self.__GetKey(),
                "name": "",
                "release_date": "",
                "is_available": False,
                "size": ""
            }
        else:
            return {
                "key": self.__GetKey(),
                "name": self.__GetName(),
                "release_date": self.__GetReleaseDate(),
                "is_available": True,
                "size": self.__GetSize()
            }
