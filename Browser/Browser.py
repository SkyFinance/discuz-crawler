from Browser.WebDriverInitializer.Impl.ChromeWebDriverInitializer import ChromeWebDriverInitializer
from Browser.WebDriverInitializer.Impl.EdgeWebDriverInitializer import EdgeWebDriverInitializer
from selenium.webdriver.support.wait import WebDriverWait
from ConfigLoader import ConfigLoader
from Utils.JavaScriptUtil import JavaScriptUtil
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC

class Browser:
    def __init__(self) -> None:
        config  = ConfigLoader()
        driverType = config.GetDriverType()
        if(driverType == "Edge"):
            self.driver = EdgeWebDriverInitializer().GetWebDriver()
        elif(driverType == "Chrome"):
            self.driver = ChromeWebDriverInitializer().GetWebDriver()
    
    def DeleteAllCookies(self) -> None:
        self.driver.delete_all_cookies()

    def AddCookies(self, cookies:dict,domain:str) -> None:
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
    
    def Get(self,url:str) -> None:
        """Get方法

        Args:
            url ([type]): Get访问的url
        """
        self.driver.get(url)

    def ScrollToBottom(self):
        JavaScriptUtil.ScrollToBottom(self.driver)

    def FindElementByName(self,name:str):
        return self.driver.find_element(By.NAME,name)

    def FindElementXpath(self,xpath:str):
        return self.driver.find_element(By.XPATH,xpath)

    def WaitUtilToClickByXpath(self,xpath:str)->None:
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath))).click()