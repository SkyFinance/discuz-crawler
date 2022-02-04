'''
Author: Nancycycycy
Date: 2022-01-24 21:05:54
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 13:27:06
Description: 帖子状态检测模块

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''
import asyncio

from merry import Merry
from tenacity import retry
from tenacity.wait import wait_random
from utils.AsyncRequest import AsyncRequest
from utils.ConfigLoader import ConfigLoader
from utils.CookieUtil import CookieUtil
from utils.DataStore import DataStore
from utils.Logging import Logging
from utils.PageParser import PageParser

merry = Merry()
logger = Logging()


class PostStatusDetector:

    def __init__(self) -> None:
        self.results = []

    def BuildPostUrl(self, post: int) -> str:
        return f"https://live.acgyouxi.xyz/thread-{post}-1-1.html"

    @retry(wait=wait_random(min=1, max=2))
    async def GetPostStatus(self, post: str) -> None:
        url = self.BuildPostUrl(post)
        response = await AsyncRequest.Get(
            url=url,
            cookies=CookieUtil.CookiesToDict(
                ConfigLoader.Get()["cookies"]["site"]),
            semaphore=asyncio.Semaphore(
                ConfigLoader.Get()["crawler"]["semaphore"]))
        result = PageParser.AnalyzePage(response, url, post)
        self.results.append(result)
        if (len(self.results) % 100 == 0):
            self.SavePostStatus()
        config = ConfigLoader.Get()["crawler"]
        threads = config["thread_max"] + 1 - config["thread_min"]
        logger.Success(
            f"threadId:{post},result: Success ({len(self.results)}/{threads})")

    def SavePostStatus(self) -> None:
        DataStore().SaveVOs("./data/status.csv", self.results)
        logger.Info("results have been saved to ./data/status.csv")

    def StartCorotinue(self) -> None:
        loop = asyncio.get_event_loop()
        config = ConfigLoader.Get()["crawler"]
        tasks = [
            self.GetPostStatus(post)
            for post in range(config["thread_min"], config["thread_max"] + 1)
        ]
        loop.run_until_complete(asyncio.wait(tasks))
        self.SavePostStatus()
