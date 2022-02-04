'''
Author: Nancycycycy
Date: 2022-02-04 21:19:39
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 21:29:52
Description: 检查网盘文件状态

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''
from dataclasses import dataclass


@dataclass
class FileStatus:
    url: str = "",
    title: str = "",
    name: str = "",
    isAvailable: str = ""
