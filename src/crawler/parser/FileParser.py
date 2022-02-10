'''
Author: Yaaprogrammer
Date: 2022-02-09 17:21:52
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 22:08:05

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from crawler.parser.BaseParser import BaseParser


class FileParser(BaseParser):

    def __init__(self, html: str) -> None:
        super().__init__(html)

    def __GetName(self):
        pattern = r'(?<=<span class="fileName">).*?(?=</span>)'
        fileName = self.ReSearchFromHtml(pattern, self.html)
        return fileName

    def __GetSize(self):
        pattern = r'(?<=文件大小：).*?(?=</span>)'
        fileSize = self.ReSearchFromHtml(pattern, self.html)
        return fileSize

    def __GetReleaseDate(self):
        pattern = r'(?<=上传日期：).*?(?=</span>)'
        fileSize = self.ReSearchFromHtml(pattern, self.html)
        return fileSize

    def __IsAvailable(self):
        return self.html.find("文件大小") != -1

    def GetResult(self):
        return {
            "name": self.__GetName(),
            "release_date": self.__GetReleaseDate(),
            "is_available": self.__IsAvailable(),
            "size": self.__GetSize()
        }
