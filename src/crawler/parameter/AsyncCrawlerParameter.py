'''
Author: Yaaprogrammer
Date: 2022-02-09 16:52:28
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-11 22:22:21

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from crawler.parser.BaseParser import BaseParser
from crawler.pipeline.BasePipeline import BasePipeline


class AsyncCrawlerParameter:

    def __init__(self, urlList: list, cookies: dict, pipeline: BasePipeline, parser: BaseParser) -> None:
        self.urlList = urlList
        self.cookies = cookies
        self.pipeline = pipeline
        self.parser = parser
