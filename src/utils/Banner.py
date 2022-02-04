'''
Author: Nancycycycy
Date: 2022-01-27 18:26:33
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 15:16:40
Description: 控制台打印横幅

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''


class Banner:
    content = ""

    def __init__(self) -> None:
        with open('./src/resource/banner.txt', "r", encoding="utf-8") as f:
            rows = f.readlines()
            self.content = self.CombineRows(rows)

    def GetContent(self):
        return self.content

    def CombineRows(self, rows):
        result = ""
        for row in rows:
            result += row
        return result
