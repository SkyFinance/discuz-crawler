'''
Author: Yaaprogrammer
Date: 2022-01-23 16:24:14
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 21:26:19
Description: 飞猫云盘转存模块

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
import queue
from threading import Lock, Thread, current_thread
from time import sleep

from browser.Browser import Browser
from merry import Merry
from model.File import File
from utils.Configuration import Configuration
from utils.CookieUtil import CookieUtil
from utils.Logging import Logging

logger = Logging()
merry = Merry()


class FeiMaoDiskTransferor:

    def __init__(self) -> None:
        self.taskFiles = self.GetDownloadTasks()
        self.CleanCaptcha()

    def GetDownloadTasks(self):
        taskQueue = queue.Queue()
        availableFiles = File.select().where(File.isAvailable == 1)
        for file in availableFiles:
            taskQueue.put(file)
        return taskQueue

    def LoginFeimao(self, browser: Browser):
        browser.Get('https://www.feimaoyun.com/home')
        browser.AddCookies(
            CookieUtil.CookiesToDict(
                Configuration.GetProperty("cookies.feimao")),
            "www.feimaoyun.com")
        logger.Success(f"thread:{current_thread().ident},login feimao success")

    def ClickDownloadButton(self, browser: Browser):
        browser.WaitUtilToClickByXpath(
            '/html/body/div/section/section/div[2]/div/div[9]/div[5]/div')
        logger.Info(f"thread:{current_thread().ident},Downlad button clicked")

    def Process(self):
        browser = Browser()
        self.LoginFeimao(browser)
        while self.taskFiles.qsize() > 0:
            with Lock():
                file = self.taskFiles.get()
            browser.Get("https://www.feimaoyun.com/s/03mx1nqt")
            self.ClickDownloadButton(browser)
            while True:
                sleep(1)

    def StartTasks(self):
        threadList = []
        for t in range(Configuration.GetProperty("driver.threads")):
            thread = Thread(target=self.Process)
            threadList.append(thread)
            thread.start()
