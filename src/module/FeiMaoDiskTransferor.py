import queue
from threading import Thread,Lock
from time import sleep
from browser.Browser import Browser
from utils.ConfigLoader import ConfigLoader
from data_store.DataStore import DataStore
from browser.controller.ImageSaveController import ImageSaveController
from utils.CookieUtil import CookieUtil
class FeiMaoDiskTransferor:
    def __init__(self) -> None:
        self.taskPosts = self.GetTransferTasks()

    def GetTransferTasks(self):
        taskQueue = queue.Queue()
        for post in filter(lambda status:len(status.feiMao)>0,DataStore().ReadVOs("./data/status.csv")):
            taskQueue.put(post)
        return taskQueue

    def LoginFeimao(self,browser):
        browser.Get('https://www.feimaoyun.com/home')
        browser.AddCookies(CookieUtil.CookiesToDict(ConfigLoader.Get()["cookies"]["feimao"]), "www.feimaoyun.com")

    def TransforPan(self,browser):
        lock = Lock()
        with lock:
            post = self.taskPosts.get()
        
        browser.WaitUtilToClickByXpath('//*[@id="main-body"]/div/div[8]/div[4]/div[3]/span[1]')
        browser.FindElementXpath('/html/body/div/section/section/div[2]/div/div[8]/div[1]/div[2]/button').click()
        browser.FindElementXpath('/html/body/div[2]/div[2]/div[4]/div[3]').click()
            
    def Process(self):
        browser = Browser()
        self.LoginFeimao(browser)
        self.TransforPan(browser)

    def StartTasks(self):
        threadList = []
        for i in range(ConfigLoader.Get()["driver"]["threads"]):
            thread = Thread(target=self.Process)
            threadList.append()
            thread.start()
        


