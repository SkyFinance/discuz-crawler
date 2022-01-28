import asyncio
from utils.Logging import Logging
from utils.AsyncRequest import AsyncRequest
from utils.ConfigLoader import ConfigLoader
from data_store.DataStore import DataStore
from tenacity import retry
from utils.PageParser import PageParser
from exceptions.StatusDetectError import StatusDetctError
from merry import Merry
from tenacity.wait import wait_random

merry = Merry()
logger = Logging()

class PostStatusDetector:
    def __init__(self) -> None:
        config = ConfigLoader()
        self.cookie = config.GetSiteCookie()
        self.threadMin = config.GetThreadMin()
        self.threadMax = config.GetThreadMax()
        self.threads = self.threadMax-self.threadMin + 1
        self.results = []

    def AutoSave(self) ->None:
        self.SavePostStatus()

    def BuildPostUrl(self, post:int) ->str:
        return f"https://live.acgyouxi.xyz/thread-{post}-1-1.html"

    """ @retry(wait=wait_random(min=1, max=2)) """
    async def GetPostStatus(self, post:str)->None:
        url = self.BuildPostUrl(post)
        response = await AsyncRequest.Get(url=url,cookies=self.cookie,semaphore=asyncio.Semaphore(100))
        result = PageParser.AnalyzePage(response,url,post)
        self.results.append(result)
        logger.Info(f"threadId:{post},result: Success ({len(self.results)}/{self.threads})")

    def SavePostStatus(self) -> None:
        DataStore().SaveVOs("./data/status.csv",self.results)
        logger.Info(f"results have been saved to ./data/status.csv")
            
    def StartCorotinue(self) -> None:
        loop = asyncio.get_event_loop()
        logger.Info(f"开始")
        tasks = [self.GetPostStatus(post) for post in range(self.threadMin,self.threadMax+1)]
        loop.run_until_complete(asyncio.wait(tasks))
        self.SavePostStatus()

def main():
    detector = PostStatusDetector()
    detector.StartCorotinue()

if(__name__ == "__main__"):
    main()
