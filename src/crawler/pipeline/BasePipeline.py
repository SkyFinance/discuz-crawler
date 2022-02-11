'''
Author: Yaaprogrammer
Date: 2022-02-11 22:16:46
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-11 22:47:29

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from abc import abstractmethod


class BasePipeline:

    @abstractmethod
    def InitCrawler(self):
        pass

    @abstractmethod
    def ItemProcessing(self, parsedResult, completed):
        pass

    @abstractmethod
    def DoneCrawler(self):
        pass
