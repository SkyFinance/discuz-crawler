'''
Author: Yaaprogrammer
Date: 2022-01-27 18:26:33
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 21:15:54
Description: 封装日志类

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''

import datetime
import os

from loguru import logger


class Logging:
    __instance = None
    DATE = datetime.datetime.now().strftime('%Y-%m-%d')
    logPath = os.path.join(os.path.dirname(os.getcwd()), "logs")
    if not os.path.isdir(logPath):
        os.makedirs(logPath)
    logger.add(
        f'{logPath}\\{DATE}.log',
        format="{time:YYYY-MM-DD HH:mm:ss}  | {level}> {elapsed}  | {message}",
        encoding='utf-8',
        retention='1 days',
        backtrace=True,
        diagnose=True,
        enqueue=True,
    )

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Logging, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def Info(self, msg, *args, **kwargs):
        return logger.info(msg, *args, **kwargs)

    def Debug(self, msg, *args, **kwargs):
        return logger.debug(msg, *args, **kwargs)

    def Warning(self, msg, *args, **kwargs):
        return logger.warning(msg, *args, **kwargs)

    def Error(self, msg, *args, **kwargs):
        return logger.error(msg, *args, **kwargs)

    def Success(self, msg, *args, **kwargs):
        return logger.success(msg, *args, **kwargs)

    def Exception(self, msg, *args, excInfo=True, **kwargs):
        return logger.exception(msg, *args, exc_info=excInfo, **kwargs)
