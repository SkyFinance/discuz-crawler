'''
Author: Yaaprogrammer
Date: 2022-02-11 22:19:59
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 16:16:06

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

        if (len(Post.select().where(
                Post.threadId == parsedResult['thread_id'])) == 0):
            Post.get_or_create(isAvailable=parsedResult['is_available'],
                               isLocked=parsedResult['is_locked'],
                               threadId=parsedResult['thread_id'],
                               hasResource=parsedResult['has_resource'])
        else:
            Post(isAvailable=parsedResult['is_available'],
                 isLocked=parsedResult['is_locked'],
                 threadId=parsedResult['thread_id'],
                 hasResource=parsedResult['has_resource']).save()

        if (parsedResult['is_available'] is True):
            if (len(PostDetail.select().where(
                    PostDetail.threadId == parsedResult['thread_id'])) == 0):
                PostDetail.get_or_create(threadId=parsedResult['thread_id'],
                                         title=parsedResult['title'],
                                         forumId=parsedResult['forum_id'])
            else:
                PostDetail(threadId=parsedResult['thread_id'],
                           title=parsedResult['title'],
                           forumId=parsedResult['forum_id']).save()

        if (parsedResult['is_available'] is True
                and parsedResult['is_locked'] is False
                and parsedResult['has_resource'] is True):
            if (len(File.select().where(
                    File.associatedPost == parsedResult['thread_id'])) == 0):
                File.get_or_create(
                    key=parsedResult['key'],
                    associatedPost=parsedResult['thread_id'],
                    passwordUnzip=parsedResult['password_unzip'],
                    isAvailable=False)
            else:
                File(key=parsedResult['key'],
                     associatedPost=parsedResult['thread_id'],
                     passwordUnzip=parsedResult['password_unzip'],
                     isAvailable=False).save()
        logger.Info(
            f"thread_id: {parsedResult['thread_id']} completed {completed}", )

    def DoneCrawler(self):
        logger.Info('Done')
