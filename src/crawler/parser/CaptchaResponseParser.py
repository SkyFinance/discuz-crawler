'''
Author: Yaaprogrammer
Date: 2022-02-10 20:36:58
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 22:20:36

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from crawler.parser.BaseParser import BaseParser
from enums.CaptchaResponse import CaptchaResponse


class CaptchaResponseParser(BaseParser):

    def __init__(self, html: str):
        super.__init__(html)

    def __ParseCaptchaResponse(self) -> CaptchaResponse:
        if (self.html.find("该文件已在橘猫云目录中") != -1 or self.html.find("转存成功") != -1):
            return CaptchaResponse.success
        else:
            return CaptchaResponse.unknown

    def GetResult(self):
        return self.__ParseCaptchaResponse()
