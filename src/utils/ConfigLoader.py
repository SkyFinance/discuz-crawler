'''
Author: Nancycycycy
Date: 2022-01-27 18:26:33
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 15:22:04
Description: 配置加载类

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''


from yaml import FullLoader, load


class ConfigLoader:

    @staticmethod
    def Get() -> None:
        return Config().ReadData()


def singleton(cls, *args, **kw):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


@singleton
class Config:

    def __init__(self) -> None:
        with open('./src/resource/config.yml', encoding="utf-8") as f:
            self.data = load(f, Loader=FullLoader)

    def ReadData(self):
        return self.data
