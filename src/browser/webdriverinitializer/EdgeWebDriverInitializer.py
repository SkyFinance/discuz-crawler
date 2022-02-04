'''
Author: Nancycycycy
Date: 2022-01-27 18:26:33
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 21:31:43
Description: Edge驱动初始化

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''
from msedge.selenium_tools import Edge, EdgeOptions
from utils.ConfigLoader import ConfigLoader


class EdgeWebDriverInitializer():

    def GetWebDriver(self) -> Edge:
        """返回Edge浏览器对象

        Returns:
            Edge: Edge浏览器对象
        """
        options = EdgeOptions()
        options.use_chromium = True
        options.binary_location = ConfigLoader.Get()["edge"]["bin_path"]
        driver = Edge(options=options, executable_path=ConfigLoader.Get()["driver"]["path"])
        return driver
