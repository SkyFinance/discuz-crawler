'''
Author: Nancycycycy
Date: 2022-01-24 21:05:54
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 22:35:21
Description: 帖子状态检测模块

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''
from crawler.AsyncCrawler import AsyncCrawler
from crawler.parameter.AsyncCrawlerParameter import AsyncCrawlerParameter
from crawler.parser.PostParser import PostParser
from merry import Merry
from model.Post import Post
from utils.Configuration import Configuration
from utils.CookieUtil import CookieUtil
from utils.Logging import Logging

merry = Merry()
logger = Logging()


class PostStatusDetector:

    def __init__(self) -> None:
        def itemAction(parsedResult, completed):
            print(parsedResult)

        def doneAction(results):
            print("done")

        urlList = self.BuildUrlList()
        cookies = CookieUtil.CookiesToDict(Configuration.GetProperty("cookies.site"))
        parameter = AsyncCrawlerParameter(urlList=urlList,
                                          cookies=cookies,
                                          itemAction=itemAction,
                                          doneAction=doneAction,
                                          parser=PostParser)
        crawler = AsyncCrawler(parameter)
        crawler.Start()

    def BuildUrlList(self) -> str:
        threadMin = Configuration.GetProperty("crawler.thread_min")
        threadMax = Configuration.GetProperty("crawler.thread_max")
        return [
            f"https://live.acgyouxi.xyz/thread-{post}-1-1.html"
            for post in range(threadMin, threadMax + 1)
        ]
