'''
Author: Yaaprogrammer
Date: 2022-02-04 19:02:31
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-04 19:04:11
Description: 验证码返回状态

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from enum import Enum


class CaptchaResponse(Enum):
    success = 1,
    robotDetected = 2,
    wrongPosition = 3,
    unknown = 4
