import re

from enums.CommentResponse import CommentResponse

class PageParser:

    @staticmethod
    def AnalyzePage(html, url, post):
        result = {}
        result["url"] = url
        result["post"] = post
        result["title"] = PageParser.GetTitle(html)
        result["isAvailable"] = PageParser.IsAvailable(html)
        result["isLocked"] = PageParser.IsLocked(html)
        result["feiMao"] = PageParser.GetFeiMaoPan(html)
        result["unZip"] = PageParser.GetUnZip(html)
        result["tid"] = PageParser.GetTid(html)
        result["fid"] = PageParser.GetFid(html)
        result["formhash"] = PageParser.GetFormHash(html)
        return result

    @staticmethod
    def ReSearchFromHtml(pattern, html):
        matchObject = re.search(pattern, html)
        if(matchObject):
            return matchObject.group()
        else:
            return ""

    @staticmethod
    def IsAvailable(html: str) -> bool:
        return html.find("抱歉，指定的主题不存在或已被删除或正在被审核") == -1 or html.find("抱歉，您没有权限访问该版块")

    @staticmethod
    def IsLocked(html: str) -> bool:
        return html.find("如果您要查看本帖隐藏内容请") != -1

    @staticmethod
    def GetFeiMaoPan(html: str) -> str:
        return PageParser.ReSearchFromHtml(r"http://(www.)?fmpan.com/s/[^\"]*", html)

    @staticmethod
    def GetUnZip(html: str) -> str:
        return PageParser.ReSearchFromHtml(r"解压密码[^\"|“|”|<]*", html)

    @staticmethod
    def GetTitle(html: str) -> str:
        return PageParser.ReSearchFromHtml(r'(?<=<span id="thread_subject">).*?(?=</span>)', html)

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
    def ParseCommentResponse(self,html:str) -> bool:
        if(html.find("回复发布成功") != -1):
            return CommentResponse.success
        elif(html.find("抱歉，您所在的用户组每小时限制发回帖")!= -1):
            return CommentResponse.perHourLimit
        elif(html.find("抱歉，您两次发表间隔少于") != -1):
            return CommentResponse.intervalLimit
        