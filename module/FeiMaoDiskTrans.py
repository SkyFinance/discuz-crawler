from time import sleep
from browser.Browser import Browser
from utils.ConfigLoader import ConfigLoader
from data_store.DataStore import DataStore

class FeiMaoDiskTrans:
    def __init__(self) -> None:
        self.browser = Browser()
        self.config = ConfigLoader()
        self.Simulate()

    def GetDiskUrls():
        dataStore = DataStore()
        lines=dataStore.ReadLines("./data/status.csv")
        posts = []
        for line in lines:
            if(line["feiMao"]):
                post = {}
                post["title"] = line["title"]
                post["url"] = line["feiMao"]
                posts.append(post)
        return posts

    def LoginFeimao(self):
        self.browser.Get('https://www.feimaoyun.com/home')
        self.browser.AddCookies(
            self.config.GetFeiMaoCookie(), "www.feimaoyun.com")

    def TransforPan(self):
        self.browser.WaitUtilToClickByXpath(
            '//*[@id="main-body"]/div/div[8]/div[4]/div[3]/span[1]')
        sleep(1)
        self.browser.FindElementXpath(
            '/html/body/div/section/section/div[2]/div/div[8]/div[1]/div[2]/button').click()

    def Simulate(self):
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
        


def main():
    crawler = FeiMaoDiskTrans()


if __name__ == "__main__":
    main()
