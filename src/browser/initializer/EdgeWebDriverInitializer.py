'''
Author: Yaaprogrammer
Date: 2022-01-27 18:26:33
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 20:47:27
Description: Edge驱动初始化

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from browser.initializer.BaseWebDriverInitializer import \
    BaseWebDriverInitializer
from msedge.selenium_tools import Edge, EdgeOptions
from utils.Configuration import Configuration


class EdgeWebDriverInitializer(BaseWebDriverInitializer):

    def GetWebDriver(self) -> Edge:
        """返回Edge浏览器对象

        Returns:
            Edge: Edge浏览器对象
        """
        options = EdgeOptions()
        options.use_chromium = True
        options.binary_location = Configuration.GetProperty("edge.bin_path")
        driver = Edge(options=options, executable_path=Configuration.GetProperty("driver.path"))
        return driver
