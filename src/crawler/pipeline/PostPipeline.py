'''
Author: Yaaprogrammer
Date: 2022-02-11 22:19:59
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-11 23:07:59

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from crawler.pipeline.BasePipeline import BasePipeline
from model.File import File
from model.Post import Post
from model.PostDetail import PostDetail
from utils.Logging import Logging

logger = Logging()


class PostPipeline(BasePipeline):

    def InitCrawler(self):
        pass

    def ItemProcessing(self, parsedResult, completed):
        Post.create(isAvailable=parsedResult['is_available'],
                    isLocked=parsedResult['is_locked'],
                    threadId=parsedResult['thread_id']).execute()
        PostDetail.create(threadId=parsedResult['thread_id'],
                          title=parsedResult['title'],
                          forumId=parsedResult['forum_id']).execute()
        File.create(key=parsedResult['key'],
                    associatedPost=parsedResult['thread_id'],
                    passwordUnzip=parsedResult['password_unzip']).execute()
        logger.Info(
            f"thread_id: {parsedResult['thread_id']} completed {completed}", )

    def DoneCrawler(self):
        logger.Info('Done')
