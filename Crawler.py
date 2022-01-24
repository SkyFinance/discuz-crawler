import base64
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from .Utils.SliderUtil import SliderUtil
import yaml
from os import path

import requests

class Crawler:
    def __init__(self) -> None:
        self.LoadConfig()
        self.CreateBrowser()
        self.Simulate()

    def CheckAvailablePosts():

        pass
    def LoadConfig(self):
        if(path.exists('config.yml')):
            self.ReadConfigData()

    def ReadConfigData(self):
        with open('config.yml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.driver = data['driver']
            self.siteCookies = self.CookiesToDict(data['cookies']['site'])
            self.feimaoCookies = self.CookiesToDict(data['cookies']['feimao'])

    def CreateBrowser(self):
        desiredCapabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desiredCapabilities["pageLoadStrategy"] = "none"
        driverService = Service(self.driver)
        self.browser = webdriver.Chrome(service=driverService)
        """ self.browser.implicitly_wait(5) """


    

    def AddCookies(self, cookies,domain):
        for key, value in cookies.items():
            self.browser.add_cookie({
                'name': key,
                "value": value,
                'domain': domain,
            })

    def SaveBackGrounds(self):
        getBackGroundScript = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
        getFullBackGroundScript = 'return document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")[0].toDataURL("image/png");'
        imgInfo = self.browser.execute_script(getBackGroundScript)
        imgBase64 = imgInfo.split(',')[1]
        imgBytes = base64.b64decode(imgBase64)
        with open('bg.png','wb') as f: 
            f.write(imgBytes)
        imgInfo = self.browser.execute_script(getFullBackGroundScript) 
        imgBase64 = imgInfo.split(',')[1] 
        imgBytes = base64.b64decode(imgBase64)  
        with open('fullbg.png','wb') as f:  
            f.write(imgBytes)
    
    def Transaction(self,post):
        self.ViewPost(post)
        self.CommentPost()
        self.ClickPanUrl()
        self.TransforPan()

    def ViewPost(self,post):
        self.browser.get('https://live.acgyouxi.xyz/thread-'+str(post)+'-1-1.html')
    
    def CommentPost(self):
        getBackGroundScript = "var q=document.documentElement.scrollTop=100000"
        self.browser.execute_script(getBackGroundScript)
        self.browser.find_element_by_name(
            "message").send_keys("66666666666666666")
        self.browser.find_element_by_name('replysubmit').click()
        sleep(5)

    def ClickPanUrl(self):
        panUrl = self.browser.find_element_by_xpath("/html/body/div[10]/div/div[4]/div[2]/div[1]/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/table/tbody/tr/td/div/font/strong/a[1]").text
        self.browser.get(panUrl)
        sleep(2)

    def TransforPan(self):
        
        self.browser.find_element_by_xpath('//*[@id="main-body"]/div/div[8]/div[4]/div[3]/span[1]').click()
        sleep(1)
        self.browser.find_element_by_xpath('/html/body/div/section/section/div[2]/div/div[8]/div[1]/div[2]/button').click()
        sleep(3)

    def InitCookies(self):
        self.LoginSite()
        self.LoginFeimao()

    def LoginFeimao(self):
        self.browser.get('https://www.feimaoyun.com/home')
        self.AddCookies(self.feimaoCookies,"www.feimaoyun.com")
    
    def LoginSite(self):
        self.browser.get("https://live.acgyouxi.xyz")
        self.browser.delete_all_cookies()
        self.AddCookies(self.siteCookies,'live.acgyouxi.xyz')

    def Simulate(self):
        self.InitCookies()
        self.Transaction(11277)
        while True:
            self.SlideCaptcha()
            sleep(2)
            self.browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[3]').click()
            sleep(2)

    def SlideCaptcha(self):
        self.SaveBackGrounds()
        bgImage = Image.open('bg.png')
        fullbgImage = Image.open('fullbg.png')
        distance = self.GetDistance(bgImage,fullbgImage)
        trace = self.GenerateTracks(distance)
        slider = self.browser.find_element_by_class_name('geetest_slider_button')
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in trace['forward_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=x,yoffset=0).perform()
        for x in trace['back_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=x,yoffset=0).perform()
        ActionChains(self.browser).release().perform()

def main():
    crawler = Crawler()

if __name__ == "__main__":
    main()
