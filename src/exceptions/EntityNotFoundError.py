'''
Author: Yaaprogrammer
Date: 2022-01-28 17:24:17
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-04 15:17:50
Description: 数据实体未找到

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''


class EntityNotFoundError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return ("未找到对应VO: {}".format(repr(self.value)))
