'''
Author: Yaaprogrammer
Date: 2022-02-10 17:31:58
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 22:40:50

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from crawler.parser.BaseParser import BaseParser
from utils.Logging import Logging

logger = Logging()


class PostParser(BaseParser):
    def __init__(self, html: str):
        
        super.__init__(html)

    def __IsAvailable(self) -> bool:
        return self.html.find("抱歉，指定的主题不存在或已被删除或正在被审核") == -1 and self.html.find(
            "抱歉，您没有权限访问该版块") == -1

    def __IsLocked(self) -> bool:
        return self.html.find("如果您要查看本帖隐藏内容请") != -1

    def __GetFeimaoKey(self) -> str:
        return self.ReSearchFromHtml(r"(?<=http://(www.)?fmpan.com/s/)[^\"]*", self.html)

    def __GetPasswordUnzip(self) -> str:
        return self.ReSearchFromHtml(r"解压密码[^\"|“|”|<]*", self.html)

    def __GetTitle(self) -> str:
        return self.ReSearchFromHtml(
            r'(?<=<span id="thread_subject">).*?(?=</span>)', self.html)

    def __GetThreadId(self) -> str:
        return self.ReSearchFromHtml(r'(?<=&tid=).*?(?=&)', self.html)

    def __GetForumId(self) -> str:
        return self.ReSearchFromHtml(r'(?<=;fid=).*?(?=")', self.html)

    def __GetFormhash(self) -> str:
        return self.ReSearchFromHtml(r'(?<=;formhash=).*?(?=")', self.html)

    def GetResult(self) -> dict:
        logger.Debug("create")
        return {"thread_id": self.__GetThreadId(),
                "forum_id": self.__GetForumId(),
                "formhash": self.__GetFormhash(),
                "password_unzip": self.__GetPasswordUnzip(),
                "title": self.__GetTitle(),
                "feimao_key": self.__GetFeimaoKey(),
                "is_available": self.__IsAvailable(),
                "is_locked": self.__IsLocked()}
