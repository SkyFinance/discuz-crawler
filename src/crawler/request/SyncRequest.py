'''
Author: Yaaprogrammer
Date: 2022-01-27 18:26:33
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 22:07:55
Description: 同步请求类

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''

import requests
from merry import Merry
from tenacity import retry, stop_after_attempt, wait_random
from utils.Logging import Logging

merry = Merry()


class SyncRequest(object):

    @staticmethod
    @merry._try
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def Post(url: str, data: dict, cookies: dict) -> str:
        """同步Post方法

        Args:
            url (str): url
            data (dict): Post数据
            cookies (dict): cookies字典

        Returns:
            str: 解码后的html
        """
        response = requests.post(url=url, data=data, cookies=cookies)
        return response.text

    @staticmethod
    @merry._except(requests.exceptions.ConnectTimeout)
    def CatchConnectTimeoutError(e):
        Logging().Error('ConnectTimeoutError: ' + str(e))
        raise e

    @staticmethod
    @merry._except(requests.exceptions.ConnectionError)
    def CatchConnectionError(e):
        Logging().Error('ConnectionError: ' + str(e))
        raise e

    @staticmethod
    @merry._except(requests.exceptions.ChunkedEncodingError)
    def CatchChunkedEncodingError(e):
        Logging().Error('ChunkedEncodingError: ' + str(e))
        raise e

    @staticmethod
    @merry._except(Exception)
    def CatchAll(e):
        Logging().Error('UnknownError: ' + str(e))
        raise e
