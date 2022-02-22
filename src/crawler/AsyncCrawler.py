'''
Author: Yaaprogrammer
Date: 2022-02-09 16:33:05
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 18:30:35

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
import asyncio

from utils.Configuration import Configuration
from utils.Logging import Logging

from crawler.BaseCrawler import BaseCrawler
from crawler.request.AsyncRequest import AsyncRequest

logger = Logging()


class AsyncCrawler(BaseCrawler):

    def Start(self):
        loop = asyncio.get_event_loop()
        tasks = []
        urlIndex = 0
        for url in self.parameter.urlList:
            data = self.parameter.dataList[urlIndex]
            urlIndex = urlIndex + 1
            tasks.append(self.ExecuteTask(url, data))
        self.parameter.pipeline.InitCrawler()
        loop.run_until_complete(asyncio.wait(tasks))
        self.parameter.pipeline.DoneCrawler()

    async def ExecuteTask(self, url, data={}) -> None:
        if (self.parameter.method == "GET"):
            response = await AsyncRequest.Get(
                url=url,
                cookies=self.parameter.cookies,
                semaphore=asyncio.Semaphore(
                    Configuration.GetProperty("crawler.semaphore")))
        elif (self.parameter.method == "POST"):
            response = await AsyncRequest.Post(
                url=url,
                data=data,
                cookies=self.parameter.cookies,
                semaphore=asyncio.Semaphore(
                    Configuration.GetProperty("crawler.semaphore")))
        self.HandleResponse(url, data, response)
