from lxml import etree
import aiohttp
import asyncio
from ConfigLoader import ConfigLoader

class AvailablePostChecker:
    def __init__(self) -> None:
        self.semaphore = asyncio.Semaphore(10)
        self.cookie = ConfigLoader().GetSiteCookie()
        pass

    def BuildPostUrls(self):
        urls = []
        for i in range(100,110):
            urls.append(f"https://live.acgyouxi.xyz/thread-{i}-1-1.html")
        return urls
    
    def IsAvailable(self,html):
        selector = etree.HTML(html)
        pass

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