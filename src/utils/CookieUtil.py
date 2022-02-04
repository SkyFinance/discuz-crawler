'''
Author: Nancycycycy
Date: 2022-01-27 18:26:33
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 13:01:18
Description: Cookie工具

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''


class CookieUtil:

    @staticmethod
    def CookiesToDict(cookiesString: str) -> dict:
        """将从浏览器获得的字符串的Cookie整合为字典形式

        Args:
            cookiesString (str): 从浏览器获得的Cookie字符串

        Returns:
            dict: Cookie字典
        """
        cookies = {}
        for data in cookiesString.split("; "):
            key = data.split('=', 1)[0]  # (以'='切割，1为切割1次)
            value = data.split('=', 1)[1]
            cookies[key] = value
        return cookies
