'''
Author: Nancycycycy
Date: 2022-01-23 16:24:14
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 21:18:48
Description: 飞猫云盘转存模块

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''
import os
import queue
import shutil
from threading import Lock, Thread, current_thread
from time import sleep

from browser.Browser import Browser
from browser.controller.ImageSaveController import ImageSaveController
from browser.controller.SliderController import SliderController
from enums.CaptchaResponse import CaptchaResponse
from merry import Merry
from utils.ConfigLoader import ConfigLoader
from utils.CookieUtil import CookieUtil
from utils.DataStore import DataStore
from utils.Logging import Logging
from utils.PageParser import PageParser

logger = Logging()
merry = Merry()


class FeiMaoDiskTransferor:

    def __init__(self) -> None:
        self.taskPosts = self.GetTransferTasks()
        self.CleanCaptcha()

    def GetTransferTasks(self):
        taskQueue = queue.Queue()
        for post in filter(lambda status: len(status.feiMao) > 0,
                           DataStore().ReadEntities("./src/data/status.csv")):
            taskQueue.put(post)
        return taskQueue

    def CleanCaptcha(self):
        shutil.rmtree('./src/captcha')
        os.mkdir('./src/captcha')

    def LoginFeimao(self, browser):
        browser.Get('https://www.feimaoyun.com/home')
        browser.AddCookies(
            CookieUtil.CookiesToDict(ConfigLoader.Get()["cookies"]["feimao"]),
            "www.feimaoyun.com")
        logger.Success(f"thread:{current_thread().ident},login feimao success")

    def CloseAd(self, browser: Browser):
        browser.WaitUtilToClickByXpath(
            '//*[@id="main-body"]/div/div[8]/div[4]/div[3]/span[1]')
        logger.Info(f"thread:{current_thread().ident},Ad closed")

    def ClickTransferButton(self, browser: Browser):
        browser.WaitUtilToClickByXpath(
            '/html/body/div/section/section/div[2]/div/div[8]/div[1]/div[2]/button'
        )
        logger.Info(f"thread:{current_thread().ident},Transfer button clicked")
        sleep(10)

    def SaveCaptcha(self, browser: Browser):
        browser.WaitUtilByXpath(
            "/html/body/div[2]/div[2]/div[6]/div/div[1]/div[2]/div[2]")
        logger.Info(f"thread:{current_thread().ident},Captcha appeared")
        imageSaveController = ImageSaveController(browser)
        imageSaveController.SaveImageFromCanvas(
            "geetest_canvas_bg geetest_absolute", f"./src/captcha/bg_{current_thread().ident}.png")
        imageSaveController.SaveImageFromCanvas(
            "geetest_canvas_fullbg geetest_fade geetest_absolute",
            f"./src/captcha/fullbg_{current_thread().ident}.png")
        logger.Info(f"thread:{current_thread().ident},Captcha saved")

    def SlideCaptcha(self, browser: Browser):
        sliderController = SliderController(browser)
        sliderController.Slide("geetest_slider_button",
                               f"./src/captcha/bg_{current_thread().ident}.png",
                               f"./src/captcha/fullbg_{current_thread().ident}.png")

    @merry._try
    def Process(self):
        browser = Browser()
        self.LoginFeimao(browser)
        while self.taskPosts.qsize() > 0:
            with Lock():
                post = self.taskPosts.get()
            merry.g.post = post
            merry.g.transferor = self
            browser.Get(post.feiMao)
            self.CloseAd(browser)
            self.ClickTransferButton(browser)
            self.SaveCaptcha(browser)
            self.SlideCaptcha(browser)
            """ browser.WaitUtilToClickByXpath("/html/body/div[2]/div[2]/div[4]/div[3]") """
            sleep(3)
            captchaResult = PageParser.ParseCaptchaResponse(browser.GetSource())
            if(captchaResult == CaptchaResponse.success):
                logger.Success(f"thread:{current_thread().ident},Transfer success Remains:{self.taskPosts.qsize()}")
            else:
                logger.Error(f"thread:{current_thread().ident},Transfer failed Remains:{self.taskPosts.qsize()}")
                """ raise SlideError("转存失败") """

    """ @merry._except(Exception)
    def HandleException():
        post = getattr(merry.g, 'post', None)
        transferor = getattr(merry.g, 'transferor', None)
        if (post is not None and transferor is not None):
            with Lock():
                transferor.taskPosts.put(post) """

    def StartTasks(self):
        threadList = []
        for t in range(ConfigLoader.Get()["driver"]["threads"]):
            thread = Thread(target=self.Process)
            threadList.append(thread)
            thread.start()
