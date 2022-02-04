'''
Author: Nancycycycy
Date: 2022-02-04 19:02:31
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 19:04:11
Description: 验证码返回状态

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''
from enum import Enum


class CaptchaResponse(Enum):
    success = 1,
    robotDetected = 2,
    wrongPosition = 3,
    unknown = 4
