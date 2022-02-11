'''
Author: Yaaprogrammer
Date: 2022-01-27 18:26:33
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 19:49:04
Description: 配置加载类

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''


from copy import deepcopy
from threading import Lock

from yaml import FullLoader, load


class Configuration:
    _instance = None
    _lock = Lock()

    @classmethod
    def GetProperty(cls, item: str) -> None:
        with cls._lock:
            if(cls._instance is None):
                with open('./src/resource/config.yml', encoding="utf-8") as f:
                    cls._instance = load(f, Loader=FullLoader)
        config = deepcopy(cls._instance)
        for segment in item.split("."):
            config = config[segment]
        return config
