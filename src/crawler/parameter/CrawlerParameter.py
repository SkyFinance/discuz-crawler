'''
Author: Yaaprogrammer
Date: 2022-02-09 16:52:28
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 18:23:45

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from dataclasses import dataclass, field

from crawler.parser.BaseParser import BaseParser
from crawler.pipeline.BasePipeline import BasePipeline


@dataclass
class CrawlerParameter:
    urlList: list
    cookies: dict
    pipeline: BasePipeline
    parser: BaseParser
    method: str
    dataList: list = field(default_factory=list)
