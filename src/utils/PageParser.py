'''
Author: Nancycycycy
Date: 2022-01-27 18:26:33
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 19:14:03
Description: html关键信息分析

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''

import re

from entity.PostStatus import PostStatus
from enums.CaptchaResponse import CaptchaResponse
from enums.CommentResponse import CommentResponse


class PageParser:

    @staticmethod
    def AnalyzePage(html, url, post) -> PostStatus:
        return PostStatus(url=url,
                          post=post,
                          title=PageParser.GetTitle(html),
                          isAvailable=PageParser.IsAvailable(html),
                          isLocked=PageParser.IsLocked(html),
                          feiMao=PageParser.GetFeiMaoPan(html),
                          unZip=PageParser.GetUnZip(html),
                          tid=PageParser.GetTid(html),
                          fid=PageParser.GetFid(html),
                          formhash=PageParser.GetFormHash(html))

    @staticmethod
    def ReSearchFromHtml(pattern, html):
        matchObject = re.search(pattern, html)
        if (matchObject):
            return matchObject.group()
        else:
            return ""

    @staticmethod
    def IsAvailable(html: str) -> bool:
        return html.find("抱歉，指定的主题不存在或已被删除或正在被审核") == -1 and html.find(
            "抱歉，您没有权限访问该版块") == -1

    @staticmethod
    def IsLocked(html: str) -> bool:
        return html.find("如果您要查看本帖隐藏内容请") != -1

    @staticmethod
    def GetFeiMaoPan(html: str) -> str:
        return PageParser.ReSearchFromHtml(r"http://(www.)?fmpan.com/s/[^\"]*",
                                           html)

    @staticmethod
    def GetUnZip(html: str) -> str:
        return PageParser.ReSearchFromHtml(r"解压密码[^\"|“|”|<]*", html)

    @staticmethod
    def GetTitle(html: str) -> str:
        return PageParser.ReSearchFromHtml(
            r'(?<=<span id="thread_subject">).*?(?=</span>)', html)

    @staticmethod
    def GetTid(html: str) -> str:
        return PageParser.ReSearchFromHtml(r'(?<=&tid=).*?(?=&)', html)

    @staticmethod
    def GetFid(html: str) -> str:
        return PageParser.ReSearchFromHtml(r'(?<=;fid=).*?(?=")', html)

    @staticmethod
    def GetFormHash(html: str) -> str:
        return PageParser.ReSearchFromHtml(r'(?<=;formhash=).*?(?=")', html)

    @staticmethod
    def ParseCommentResponse(html: str) -> CommentResponse:
        if (html.find("回复发布成功") != -1):
            return CommentResponse.success
        elif (html.find("您所在的用户组每小时限制发回帖") != -1):
            return CommentResponse.perHourLimit
        elif (html.find("抱歉，您两次发表间隔少于") != -1):
            return CommentResponse.intervalLimit
        elif (html.find("您当前的访问请求当中含有非法字符，已经被系统拒绝")):
            return CommentResponse.illegalRequest
        else:
            return CommentResponse.unknown

    @staticmethod
    def ParseCaptchaResponse(html: str) -> CaptchaResponse:
        if (html.find("该文件已在橘猫云目录中") != -1 or html.find("转存成功") != -1):
            return CaptchaResponse.success
        else:
            return CaptchaResponse.unknown
