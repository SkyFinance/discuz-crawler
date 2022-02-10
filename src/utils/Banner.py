'''
Author: Nancycycycy
Date: 2022-01-27 18:26:33
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 20:51:41
Description: 控制台打印横幅

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''


class Banner:
    content = ""

    def __init__(self) -> None:
        with open('./src/resource/banner.txt', "r", encoding="utf-8") as f:
            rows = f.readlines()
            self.content = self.__CombineRows(rows)

    def GetContent(self):
        return self.content

    def __CombineRows(self, rows):
        result = ""
        for row in rows:
            result += row
        return result
