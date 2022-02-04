'''
Author: Nancycycycy
Date: 2022-01-26 11:44:42
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 13:05:59
Description: 评论发布模块

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''
import queue
from time import sleep

from enums.CommentResponse import CommentResponse
from exceptions.CommentIllegalRequestError import CommentIllegalRequestError
from exceptions.CommentIntervalLimitError import CommentIntervalLimitError
from exceptions.CommentPerHourLimitError import CommentPerHourLimitError
from exceptions.CommentPublishError import CommentPublishError
from merry import Merry
from utils.ConfigLoader import ConfigLoader
from utils.CookieUtil import CookieUtil
from utils.DataStore import DataStore
from utils.Logging import Logging
from utils.PageParser import PageParser
from utils.SyncRequest import SyncRequest

merry = Merry()
merry.logger.disabled = True
logger = Logging()


class CommentPublisher:

    def __init__(self) -> None:
        self.taskPosts = self.NeededToComment()
        merry.g.publisher = self

    def ReadPosts(self):
        return DataStore().ReadEntities("./data/Status.csv")

    def NeededToComment(self) -> queue.Queue:
        postList = list(
            filter(
                lambda post: post.isAvailable == "True" and post.isLocked ==
                "True", self.ReadPosts()))
        postQueue = queue.Queue()
        for post in postList:
            postQueue.put(post)
        return postQueue

    def BuildCommentUrl(self, post):
        tid = post.tid
        fid = post.fid
        return f"https://live.acgyouxi.xyz/forum.php?mod=post&action=reply&tid={tid}&fid={fid}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"

    def BuildCommentPostData(self, post):
        return {
            "message": ConfigLoader.Get()["crawler"]["comment_message"],
            "formhash": post.formhash,
            "usesig": "",
            "subject": ""
        }

    @merry._try
    def CommentPost(self, post):
        sleep(ConfigLoader.Get()["crawler"]["comment_sleep"])
        merry.g.post = post
        postData = self.BuildCommentPostData(post)
        url = self.BuildCommentUrl(post)
        cookies = CookieUtil.CookiesToDict(
            ConfigLoader.Get()["cookies"]["site"])
        response = SyncRequest.Post(cookies=cookies, url=url, data=postData)
        commentResult = PageParser.ParseCommentResponse(response)
        self.HandleCommentResult(commentResult, post)

    @merry._try
    def HandleCommentResult(self, commentResult, post):
        merry.g.post = post
        if (commentResult == CommentResponse.success):
            logger.Success(
                f"thread={post.tid} Comment Success (remains {self.taskPosts.qsize()})"
            )
        elif (commentResult == CommentResponse.perHourLimit):
            logger.Error(f"thread={post.tid} 每小时评论数量限制")
            raise CommentPerHourLimitError(post)
        elif (commentResult == CommentResponse.intervalLimit):
            logger.Error(f"thread={post.tid} 两次评论时间间隔限制")
            raise CommentIntervalLimitError(post)
        elif (commentResult == CommentResponse.illegalRequest):
            logger.Error(f"thread={post.tid} 评论含有非法字符，请检查post数据是否正常")
            raise CommentIllegalRequestError(post)
        else:
            logger.Error(f"thread={post.tid} 评论出现未知错误")
            raise CommentPublishError(post)

    @merry._except(CommentPerHourLimitError)
    def WaitForAnHour(self):
        post = getattr(merry.g, 'post', None)
        publisher = getattr(merry.g, 'publisher', None)
        if (publisher is not None and post is not None):
            publisher.taskPosts.put(post)
            logger.Info(f"触发每小时发帖限制，自动等待一小时(remains {self.taskPosts.qsize()})")
            """ sleep(60*60) """

    @merry._except(Exception)
    def HandleFailedComment(self):
        post = getattr(merry.g, 'post', None)
        publisher = getattr(merry.g, 'publisher', None)
        if (publisher is not None and post is not None):
            publisher.taskPosts.put(post)

    def StartTasks(self):
        while self.taskPosts.qsize():
            post = self.taskPosts.get()
            self.CommentPost(post)
