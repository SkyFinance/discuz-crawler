from abc import abstractmethod, ABCMeta

class WebDriverInitializer(metaclass=ABCMeta):
    @abstractmethod
    def GetWebDriver(self):
        pass