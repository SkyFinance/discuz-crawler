'''
Author: Yaaprogrammer
Date: 2022-01-27 18:26:33
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 16:53:49
Description: 异步请求类

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''

import asyncio

import aiohttp
from aiohttp import client_exceptions
from merry import Merry
from tenacity import retry, stop_after_attempt
from tenacity.wait import wait_random
from utils.Logging import Logging

merry = Merry()


class AsyncRequest(object):

    @staticmethod
    @merry._try
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    async def Get(url: str, semaphore: asyncio.Semaphore,
                  cookies: dict) -> str:
        """异步Get方法

        Args:
            url (str): url
            semaphore (asyncio.Semaphore): 信号量，控制并发连接数
            cookie (dict): cookie字典

        Returns:
            str: 解码后的html
        """
        async with semaphore:
            async with aiohttp.ClientSession(cookies=cookies) as session:
                async with session.request('GET', url) as response:
                    html = await response.read()
                    html = html.decode()
                    return html

    @staticmethod
    @merry._try
    async def Post(url: str, data: dict, semaphore: asyncio.Semaphore,
                   cookies: dict) -> str:
        """异步Post方法

        Args:
            url (str): url
            semaphore (asyncio.Semaphore): 信号量，控制并发连接数
            cookie (dict): cookie字典

        Returns:
            str: 解码后的html
        """
        async with semaphore:
            async with aiohttp.ClientSession(cookies=cookies) as session:
                async with session.request('POST', url=url,
                                           data=data) as response:
                    html = await response.read()
                    html = html.decode()
                    return html

    @staticmethod
    @merry._except(client_exceptions.ClientConnectionError)
    def CatchClientConnectionError(e):
        Logging().Error('ClientConnectionError: ' + str(e))
        raise e

    @staticmethod
    @merry._except(client_exceptions.ServerTimeoutError)
    def CatchServerTimeoutError(e):
        Logging().Error('ServerTimeoutError: ' + str(e))
        raise e

    @staticmethod
    @merry._except(Exception)
    def CatchAll(e):
        Logging().Error('UnknownError: ' + str(e))
        raise e
