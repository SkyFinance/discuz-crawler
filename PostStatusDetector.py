import aiohttp
import asyncio
from aiohttp import client_exceptions
from ConfigLoader import ConfigLoader
import re
from loguru import logger

from DataStore.DataStore import DataStore

class PostStatusDetector:
    def __init__(self) -> None:
        config = ConfigLoader()
        self.cookie = config.GetSiteCookie()
        self.threadMin = config.GetThreadMin()
        self.threadMax = config.GetThreadMax()
        self.threads = self.threadMax-self.threadMin +1
        self.semaphore = asyncio.Semaphore(50)
        self.currentResults = 0
        self.results = []
        pass
    def ReSearchFromHtml(self,pattern,html):
        matchObject = re.search(pattern,html)
        if(matchObject):
            return matchObject.group()
        else:
            return ""

    def IsAvailable(self,html:str) -> bool:
        return html.find("抱歉，指定的主题不存在或已被删除或正在被审核") == -1 or html.find("抱歉，您没有权限访问该版块")

    def IsLocked(self,html:str) -> bool:
        return html.find("如果您要查看本帖隐藏内容请") != -1

    def GetFeiMaoPan(self,html:str) -> str:
        return self.ReSearchFromHtml(r"http://(www.)?fmpan.com/s/[^\"]*",html)

    def GetUnZip(self,html:str) -> str:
        return self.ReSearchFromHtml(r"解压密码[^\"|“|”|<]*",html)

    def GetTitle(self,html:str) -> str:
        return self.ReSearchFromHtml(r'(?<=<span id="thread_subject">).*?(?=</span>)',html)

    def GetTid(self , html:str) -> str:
        return self.ReSearchFromHtml(r'(?<=&tid=).*?(?=&)',html)

    def GetFid(self , html:str) -> str:
        return self.ReSearchFromHtml(r'(?<=;fid=).*?(?=")',html)

    def GetFormHash(self , html:str) -> str:
        return self.ReSearchFromHtml(r'(?<=;formhash=).*?(?=")',html)

    async def GetPostStatus(self,post):
        url = f"https://live.acgyouxi.xyz/thread-{post}-1-1.html"
        try:
            async with self.semaphore:
                async with aiohttp.ClientSession(cookies=self.cookie) as session:
                    async with session.request('GET', url) as response:
                        html = await response.read()
                        html = html.decode()
                        result = {}
                        result["url"] = url
                        result["post"] = post
                        result["title"] = self.GetTitle(html)
                        result["isAvailable"] = self.IsAvailable(html)
                        result["isLocked"] = self.IsLocked(html)
                        result["feiMao"] = self.GetFeiMaoPan(html)
                        result["unZip"] = self.GetUnZip(html)
                        result["tid"] = self.GetTid(html)
                        result["fid"] = self.GetFid(html)
                        result["formhash"] = self.GetFormHash(html)
                        self.results.append(result)
                        logger.info(f"threadId:{post},result: Success ({len(self.results)}/{self.threads})")
                        self.currentResults += 1
                        if(self.currentResults > 100):
                            self.SavePostStatus()
                            self.currentResults = 0
                            logger.info(f"Auto save.")
        except client_exceptions.ServerTimeoutError as timeout_error:
            logger.error("request timeout error: {}, url: {}".format(timeout_error, url))
        except Exception:
            logger.error("request unknown error")
            
                    
    def SavePostStatus(self):
        dataStore = DataStore()
        headers = ["url","post","title","isAvailable","isLocked","feiMao","unZip","tid","fid","formhash"]
        dataStore.SaveLines("./Data/Status.csv",headers,self.results)

    def StartCorotinue(self):
        loop = asyncio.get_event_loop()
        tasks = [self.GetPostStatus(post) for post in range(self.threadMin,self.threadMax+1)] 
        loop.run_until_complete(asyncio.wait(tasks))
        self.SavePostStatus()
        logger.info(f"results have been saved to ./Data/Status.csv")

def main():
    detector = PostStatusDetector()
    detector.StartCorotinue()

if(__name__ == "__main__"):
    main()