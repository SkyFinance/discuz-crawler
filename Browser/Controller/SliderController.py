
from PIL import Image
from Utils.SliderUtil import SliderUtil


class SliderController:
    def __init__(self, browser) -> None:
        self.browser = browser

    def GetTrack(self) -> list:
        """获取轨迹列表

        Returns:
            list: 包含移动轨迹的列表，单位为像素
        """
        bgImage = Image.open('./Captcha/bg.png')
        fullbgImage = Image.open('./Captcha/fullbg.png')
        distance = SliderUtil.GetDistance(bgImage, fullbgImage)
        track = SliderUtil.GenerateTracks(distance)
        return track

    def Slide(self, sliderButtonClassName:str) -> None:
        """执行滑动动作

        Args:
            sliderButtonClassName (str): 滑动按钮类名
        """
        track = self.GetTrack()
        actionChains = self.browser.GetActionChains()
        slider = self.browser.FindElementByClassName(sliderButtonClassName)
        actionChains.click_and_hold(slider).perform()
        for tracks in track['forward_tracks']:
            actionChains.move_by_offset(
                xoffset=tracks, yoffset=0).perform()
        for tracks in track['back_tracks']:
            actionChains.move_by_offset(
                xoffset=tracks, yoffset=0).perform()
        actionChains.release().perform()

    pass
