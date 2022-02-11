'''
Author: Yaaprogrammer
Date: 2022-02-09 16:33:05
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-11 22:48:10

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
import asyncio

from tenacity import retry
from tenacity.wait import wait_random
from utils.Configuration import Configuration
from utils.Logging import Logging

from crawler.parameter.AsyncCrawlerParameter import AsyncCrawlerParameter
from crawler.request.AsyncRequest import AsyncRequest

logger = Logging()


class AsyncCrawler:

    def __init__(self, parameter: AsyncCrawlerParameter) -> None:
        self.parameter = parameter
        self.results = []
        self.completed = 0

    def Start(self):
        loop = asyncio.get_event_loop()
        tasks = [self.__ExecuteTask(url) for url in self.parameter.urlList]
        self.parameter.pipeline.InitCrawler()
        loop.run_until_complete(asyncio.wait(tasks))
        self.parameter.pipeline.DoneCrawler()

    @retry(wait=wait_random(min=1, max=2))
    async def __ExecuteTask(self, url) -> None:
        response = await AsyncRequest.Get(
            url=url,
            cookies=self.parameter.cookies,
            semaphore=asyncio.Semaphore(
                Configuration.GetProperty("crawler.semaphore")))
        self.parameter.parser.html = response
        result = self.parameter.parser.GetResult()
        self.results.append(result)
        self.completed += 1
        self.parameter.pipeline.ItemProcessing(parsedResult=result,
                                               completed=self.completed)
