'''
Author: Yaaprogrammer
Date: 2022-01-24 21:05:54
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-11 23:09:56
Description: 帖子状态检测模块

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from crawler.AsyncCrawler import AsyncCrawler
from crawler.parameter.AsyncCrawlerParameter import AsyncCrawlerParameter
from crawler.parser.PostParser import PostParser
from crawler.pipeline.PostPipeline import PostPipeline
from merry import Merry
from utils.Configuration import Configuration
from utils.CookieUtil import CookieUtil
from utils.Logging import Logging

merry = Merry()
logger = Logging()


class PostStatusDetector:

    def __init__(self) -> None:

        urlList = self.BuildUrlList()
        cookies = CookieUtil.CookiesToDict(
            Configuration.GetProperty("cookies.site"))
        pipeline = PostPipeline()
        parser = PostParser()
        parameter = AsyncCrawlerParameter(urlList=urlList,
                                          cookies=cookies,
                                          pipeline=pipeline,
                                          parser=parser)
        self.crawler = AsyncCrawler(parameter)

    def BuildUrlList(self) -> str:
        threadMin = Configuration.GetProperty("crawler.thread_min")
        threadMax = Configuration.GetProperty("crawler.thread_max")
        return [
            f"https://live.acgyouxi.xyz/thread-{post}-1-1.html"
            for post in range(threadMin, threadMax + 1)
        ]

    def Start(self) -> None:
        self.crawler.Start()
