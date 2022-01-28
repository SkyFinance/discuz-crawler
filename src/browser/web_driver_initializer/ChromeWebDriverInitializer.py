from webbrowser import Chrome

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from utils.ConfigLoader import ConfigLoader


class ChromeWebDriverInitializer():

    def GetWebDriver(self) -> Chrome:
        """返回Chrome浏览器对象

        Returns:
            Chrome: Chrome浏览器对象
        """
        desiredCapabilities = DesiredCapabilities.CHROME
        driver = webdriver.Chrome(desired_capabilities=desiredCapabilities,executable_path=ConfigLoader.Get()["driver"]["path"])
        return driver