'''
Author: Yaaprogrammer
Date: 2022-02-10 20:36:31
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 22:19:17

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from crawler.parser.BaseParser import BaseParser
from enums.CommentResponse import CommentResponse


class CommentResponseParser(BaseParser):

    def __init__(self, html: str):
        super.__init__(html)

    def __ParseCommentResponse(self) -> CommentResponse:
        if (self.html.find("回复发布成功") != -1):
            return CommentResponse.success
        elif (self.html.find("您所在的用户组每小时限制发回帖") != -1):
            return CommentResponse.perHourLimit
        elif (self.html.find("抱歉，您两次发表间隔少于") != -1):
            return CommentResponse.intervalLimit
        elif (self.html.find("您当前的访问请求当中含有非法字符，已经被系统拒绝")):
            return CommentResponse.illegalRequest
        else:
            return CommentResponse.unknown

    def GetResult(self):
        return self.__ParseCommentResponse()
