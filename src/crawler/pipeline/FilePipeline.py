'''
Author: Yaaprogrammer
Date: 2022-02-11 22:19:59
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 19:45:08

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from crawler.pipeline.BasePipeline import BasePipeline
from model.File import File
from model.FileDetail import FileDetail
from utils.Logging import Logging

logger = Logging()


class FilePipeline(BasePipeline):

    def InitCrawler(self):
        pass

    def ItemProcessing(self, parsedResult, completed):
        query = File.update(isAvailable=parsedResult['is_available']).where(
            File.key == parsedResult['key'])
        query.execute()
        if (parsedResult['is_available']):
            associatedPost = File.select(
                File.associatedPost).where(File.key == parsedResult['key'])
            if (len(FileDetail.select().where(
                    FileDetail.associatedPost == associatedPost)) == 0):
                FileDetail.get_or_create(
                    associatedPost=associatedPost,
                    name=parsedResult['name'],
                    size=parsedResult['size'],
                    releaseDate=parsedResult['release_date'])
            else:
                FileDetail(associatedPost=associatedPost,
                           name=parsedResult['name'],
                           size=parsedResult['size'],
                           releaseDate=parsedResult['release_date']).save()
            logger.Info(f"file {parsedResult['name']} completed {completed}")

    def DoneCrawler(self):
        logger.Info('Done')
