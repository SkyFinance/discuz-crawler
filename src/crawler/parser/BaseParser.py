'''
Author: Yaaprogrammer
Date: 2022-02-09 18:08:54
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-11 22:44:39

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

    def ReSearchFromHtml(self, pattern: str, html: str):
        matchObject = search(pattern, html)
        if (matchObject):
            return matchObject.group()
        else:
            return ""

    @abstractclassmethod
    def GetResult():
        pass
