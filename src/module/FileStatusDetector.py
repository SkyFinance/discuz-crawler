'''
Author: Yaaprogrammer
Date: 2022-02-04 21:09:39
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 18:16:40
Description: 网盘文件状态检测

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from crawler.AsyncCrawler import AsyncCrawler
from crawler.parameter.CrawlerParameter import CrawlerParameter
from crawler.parser.FileParser import FileParser
from crawler.pipeline.FilePipeline import FilePipeline
from model.File import File
from utils.Configuration import Configuration
from utils.CookieUtil import CookieUtil
from utils.Logging import Logging

logger = Logging()


class FileStatusDetector:

    def __init__(self) -> None:

        urlList = self.BuildUrlList()
        dataList = self.BuildDataList()
        cookies = CookieUtil.CookiesToDict(
            Configuration.GetProperty("cookies.feimao"))
        pipeline = FilePipeline()
        parser = FileParser()
        parameter = CrawlerParameter(urlList=urlList,
                                     cookies=cookies,
                                     pipeline=pipeline,
                                     parser=parser,
                                     method="POST",
                                     dataList=dataList)
        self.crawler = AsyncCrawler(parameter)

    def BuildUrlList(self) -> str:
        return [
            "https://www.feimaoyun.com/index.php/down/new_detailv2"
            for file in File.select()
        ]

    def BuildDataList(self) -> str:
        return [{"code": file.key, "pucode": ""} for file in File.select()]

    def StartTasks(self) -> None:
        self.crawler.Start()
