'''
Author: Yaaprogrammer
Date: 2022-02-09 18:08:54
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 18:18:24

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from abc import abstractclassmethod

from regex import search
from utils.Logging import Logging

logger = Logging()


class BaseParser:

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, value):
        self.__html = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    def ReSearchFromHtml(self, pattern: str, html: str):
        matchObject = search(pattern, html)
        if (matchObject):
            return matchObject.group()
        else:
            return ""

    @abstractclassmethod
    def GetResult():
        pass
