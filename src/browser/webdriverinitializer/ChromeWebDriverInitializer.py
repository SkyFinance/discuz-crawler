'''
Author: Nancycycycy
Date: 2022-01-27 18:26:33
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 19:16:02
Description: Chrome驱动初始化

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''
from threading import current_thread
from webbrowser import Chrome

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from utils.ConfigLoader import ConfigLoader
from utils.Logging import Logging

logger = Logging()


class ChromeWebDriverInitializer():

    def GetWebDriver(self) -> Chrome:
        """返回Chrome浏览器对象

        Returns:
            Chrome: Chrome浏览器对象
        """
        desiredCapabilities = DesiredCapabilities.CHROME
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option(
            'excludeSwitches', ['enable-automation', 'enable-logging'])
        if(bool(ConfigLoader.Get()["driver"]["headless"])):
            chromeOptions.add_argument('--headless')
        driver = webdriver.Chrome(
            chrome_options=chromeOptions,
            desired_capabilities=desiredCapabilities,
            executable_path=ConfigLoader.Get()["driver"]["path"])
        logger.Success(f"thread:{current_thread().ident} init Chrome driver success")
        return driver
