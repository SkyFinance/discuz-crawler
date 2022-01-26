from webbrowser import Chrome

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from ConfigLoader import ConfigLoader
from ..WebDriverInitializer import WebDriverInitializer


class ChromeWebDriverInitializer(WebDriverInitializer):

    def GetWebDriver(self) -> Chrome:
        """返回Chrome浏览器对象

        Returns:
            Chrome: Chrome浏览器对象
        """
        config = ConfigLoader()
        desiredCapabilities = DesiredCapabilities.CHROME
        driver = webdriver.Chrome(desired_capabilities=desiredCapabilities,executable_path=config.GetDriverPath())
        return driver