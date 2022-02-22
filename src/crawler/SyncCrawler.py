'''
Author: Yaaprogrammer
Date: 2022-02-09 16:33:05
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-19 16:01:13

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from utils.Logging import Logging

from crawler.BaseCrawler import BaseCrawler
from crawler.request.SyncRequest import SyncRequest

logger = Logging()


class SyncCrawler(BaseCrawler):

    def Start(self):
        tasks = [self.ExecuteTask(url) for url in self.parameter.urlList]
        self.parameter.pipeline.InitCrawler()
        for task in tasks:
            task()
        self.parameter.pipeline.DoneCrawler()

    async def ExecuteTask(self, url) -> None:
        response = SyncRequest.Post(url)
        self.HandleResponse(response)
