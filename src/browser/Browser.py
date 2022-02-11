'''
Author: Yaaprogrammer
Date: 2022-01-27 18:26:33
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 20:48:26
Description: 封装浏览器类

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from time import sleep

import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from utils.Configuration import Configuration

from browser.initializer.ChromeWebDriverInitializer import \
    ChromeWebDriverInitializer
from browser.initializer.EdgeWebDriverInitializer import \
    EdgeWebDriverInitializer


class Browser:
    def __init__(self) -> None:
        driverType = Configuration.GetProperty("driver.type")
        if(driverType == "Edge"):
            self.driver = EdgeWebDriverInitializer().GetWebDriver()
        elif(driverType == "Chrome"):
            self.driver = ChromeWebDriverInitializer().GetWebDriver()

    def GetSource(self) -> str:
        return self.driver.page_source

    def DeleteAllCookies(self) -> None:
        """删除所有Cookie
        """
        self.driver.delete_all_cookies()

    def AddCookies(self, cookies: dict, domain: str) -> None:
        """为浏览器对象添加某网站的cookie
        注意要先访问过该url才能添加

        Args:
            cookies (dict): cookie字典
            domain (str): 添加cookie的网站域名
        """

        for key, value in cookies.items():
            self.driver.add_cookie({
                'name': key,
                "value": value,
                'domain': domain,
            })

    def Get(self, url: str) -> None:
        """Get方法

        Args:
            url ([type]): Get访问的url
        """
        self.driver.get(url)

    def GetDriver(self):
        """获取浏览器驱动对象

        Returns:
            webdriver: 浏览器驱动对象
        """
        return self.driver

    def GetActionChains(self):
        """获取ActionChains对象，用以模拟鼠标行为

        Returns:
            ActionChains: 模拟操作鼠标动作的对象
        """
        return ActionChains(self.driver)

    def ExecuteScript(self, script: str):
        """执行JavaScript脚本

        Args:
            script (str): JavaScript脚本字符串
        """
        return self.driver.execute_script(script=script)

    def FindElementByName(self, name: str):
        """通过name属性查找DOM元素

        Args:
            name (str): 元素name属性

        Returns:
            WebElement: 浏览器可操作的DOM元素
        """
        return self.driver.find_element(By.NAME, name)

    def FindElementByClassName(self, className: str):
        """通过class属性查找DOM元素

        Args:
            className (str): 元素class属性

        Returns:
            WebElement: 浏览器可操作的DOM元素
        """
        return self.driver.find_element(By.CLASS_NAME, className)

    def FindElementXpath(self, xpath: str) -> None:
        """通过Xpath查找DOM元素

        Args:
            xpath (str): xpath语句

        Returns:
            WebElement: 浏览器可操作的DOM元素
        """
        return self.driver.find_element(By.XPATH, xpath)

    def WaitUtilByXpath(self, xpath: str) -> None:
        """通过Xpath查找元素，等待该元素出现

        Args:
            xpath (str): Xpath语句
        """
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath)))

    def WaitUtilToClickByXpath(self, xpath: str) -> None:
        """通过Xpath查找元素，在该元素出现后再点击

        Args:
            xpath (str): Xpath语句
        """
        sleep(0.5)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        sleep(0.5)
        self.driver.find_element(By.XPATH, xpath).click()
