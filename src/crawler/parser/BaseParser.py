'''
Author: Yaaprogrammer
Date: 2022-02-09 18:08:54
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 22:07:14

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from abc import abstractclassmethod
from re import search


class BaseParser:

    def __init__(self, html: str) -> None:
        self.html = html

    def ReSearchFromHtml(self, pattern: str, html: str):
        matchObject = search(pattern, html)
        if (matchObject):
            return matchObject.group()
        else:
            return ""

    @abstractclassmethod
    def GetResult():
        pass
