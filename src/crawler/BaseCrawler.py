'''
Author: Yaaprogrammer
Date: 2022-02-19 15:52:38
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 18:19:41

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from abc import abstractmethod

from crawler.parameter.CrawlerParameter import CrawlerParameter


class BaseCrawler:

    def __init__(self, parameter: CrawlerParameter) -> None:
        self.parameter = parameter
        self.results = []
        self.completed = 0

    def HandleResponse(self, url, data, response):
        self.parameter.parser.html = response
        self.parameter.parser.url = url
        self.parameter.parser.data = data
        result = self.parameter.parser.GetResult()
        self.results.append(result)
        self.completed += 1
        self.parameter.pipeline.ItemProcessing(parsedResult=result,
                                               completed=self.completed)

    def Start(self):
        self.parameter.pipeline.InitCrawler()
        self.StartTasks()
        self.parameter.pipeline.DoneCrawler()

    @abstractmethod
    def StartTasks(self):
        pass

    @abstractmethod
    def ExecuteTask(self):
        pass
