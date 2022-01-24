from lxml import etree
import aiohttp
import asyncio
from ConfigLoader import ConfigLoader

class AvailablePostChecker:
    def __init__(self) -> None:
        self.semaphore = asyncio.Semaphore(10)
        self.cookie = ConfigLoader().GetSiteCookie()
        pass

    def BuildPostUrls(self) -> list:
        urls = []
        for i in range(1,5):
            urls.append(f"https://live.acgyouxi.xyz/thread-{i}-1-1.html")
        return urls
    
    def IsAvailable(self,html:str) -> bool:
        return html.find("抱歉，指定的主题不存在或已被删除或正在被审核") == -1

    async def GetPost(self,url):
        async with aiohttp.ClientSession(cookies=self.cookie) as session:
            async with session.request('GET', url) as response:
                html = await response.read()
                print(html.decode())

    def StartCorotinue(self):
        loop = asyncio.get_event_loop()
        tasks = [self.GetPost(url) for url in self.BuildPostUrls()] 
        loop.run_until_complete(asyncio.wait(tasks))

availablePostChecker = AvailablePostChecker()
availablePostChecker.StartCorotinue()