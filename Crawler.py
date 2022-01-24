from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from Browser.Browser import Browser
from ConfigLoader import ConfigLoader


class Crawler:
    def __init__(self) -> None:
        self.browser = Browser()
        self.config = ConfigLoader()
        self.Simulate()

    def LoginFeimao(self):
        self.browser.Get('https://www.feimaoyun.com/home')
        self.browser.AddCookies(
            self.config.GetFeiMaoCookie(), "www.feimaoyun.com")

    def LoginSite(self):
        self.browser.Get("https://live.acgyouxi.xyz")
        self.browser.DeleteAllCookies()
        self.browser.AddCookies(
            self.config.GetSiteCookie(), 'live.acgyouxi.xyz')

    def Transaction(self, post):
        self.ViewPost(post)
        self.CommentPost()
        self.ClickPanUrl()
        self.TransforPan()

    def ViewPost(self, post):
        self.browser.Get('https://live.acgyouxi.xyz/thread-' +
                         str(post)+'-1-1.html')

    def CommentPost(self):
        self.browser.ScrollToBottom()
        self.browser.FindElementByName(
            "message").send_keys("66666666666666666")
        self.browser.FindElementByName('replysubmit').click()

    def ClickPanUrl(self):
        self.browser.WaitUtilToClickByXpath(
            "/html/body/div[10]/div/div[4]/div[2]/div[1]/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/table/tbody/tr/td/div/font/strong/a[1]")

    def TransforPan(self):
        self.browser.WaitUtilToClickByXpath(
            '//*[@id="main-body"]/div/div[8]/div[4]/div[3]/span[1]')
        sleep(1)
        self.browser.FindElementXpath(
            '/html/body/div/section/section/div[2]/div/div[8]/div[1]/div[2]/button').click()

    def Simulate(self):
        self.LoginSite()
        self.LoginFeimao()
        self.Transaction(11277)
        while True:
            self.SlideCaptcha()
            sleep(2)
            self.browser.FindElementXpath(
                '/html/body/div[2]/div[2]/div[4]/div[3]').click()
            sleep(2)

    def SlideCaptcha(self):
        self.SaveBackGrounds()
        bgImage = Image.open('bg.png')
        fullbgImage = Image.open('fullbg.png')
        distance = self.GetDistance(bgImage, fullbgImage)
        trace = self.GenerateTracks(distance)
        slider = self.browser.find_element_by_class_name(
            'geetest_slider_button')
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in trace['forward_tracks']:
            ActionChains(self.browser).move_by_offset(
                xoffset=x, yoffset=0).perform()
        for x in trace['back_tracks']:
            ActionChains(self.browser).move_by_offset(
                xoffset=x, yoffset=0).perform()
        ActionChains(self.browser).release().perform()


def main():
    crawler = Crawler()


if __name__ == "__main__":
    main()
