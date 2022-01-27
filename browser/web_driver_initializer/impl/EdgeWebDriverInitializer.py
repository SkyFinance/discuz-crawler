from msedge.selenium_tools import Edge, EdgeOptions

from ConfigLoader import ConfigLoader
from ..WebDriverInitializer import WebDriverInitializer


class EdgeWebDriverInitializer(WebDriverInitializer):

    def GetWebDriver(self) -> Edge:
        """返回Edge浏览器对象

        Returns:
            Edge: Edge浏览器对象
        """
        config = ConfigLoader()
        options = EdgeOptions()
        options.use_chromium = True
        options.binary_location = config.GetEdgePath()
        driver = Edge(options=options, executable_path=config.GetDriverPath())
        return driver
