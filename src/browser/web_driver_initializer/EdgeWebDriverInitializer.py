from msedge.selenium_tools import Edge, EdgeOptions

from utils.ConfigLoader import ConfigLoader


class EdgeWebDriverInitializer():

    def GetWebDriver(self) -> Edge:
        """返回Edge浏览器对象

        Returns:
            Edge: Edge浏览器对象
        """
        config = ConfigLoader()
        options = EdgeOptions()
        options.use_chromium = True
        options.binary_location = ConfigLoader.Get()["edge"]["bin_path"]
        driver = Edge(options=options, executable_path=ConfigLoader.Get()["driver"]["path"])
        return driver
