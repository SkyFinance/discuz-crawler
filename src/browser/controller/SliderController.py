'''
Author: Nancycycycy
Date: 2022-01-27 18:26:33
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 20:21:12
Description: 滑动验证码控制器

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''
from threading import current_thread

from PIL import Image
from utils.Logging import Logging
from utils.SliderUtil import SliderUtil

logger = Logging()


class SliderController:

    def __init__(self, browser) -> None:
        self.browser = browser

    def __GetTrack(self, bgPath, fullbgPath) -> list:
        """获取轨迹列表

        Returns:
            list: 包含移动轨迹的列表，单位为像素
        """
        bgImage = Image.open(bgPath)
        fullbgImage = Image.open(fullbgPath)
        distance = SliderUtil.GetDistance(bgImage, fullbgImage)
        logger.Info(f"thread:{current_thread().ident},Gap left distance:{distance}")
        track = SliderUtil.GenerateTrack(distance)
        print(track)
        return track

    def Slide(self, sliderButtonClassName: str, bgPath, fullbgPath) -> None:
        """执行滑动动作

        Args:
            sliderButtonClassName (str): 滑动按钮类名
        """
        track = self.__GetTrack(bgPath, fullbgPath)
        actionChains = self.browser.GetActionChains()
        slider = self.browser.FindElementByClassName(sliderButtonClassName)
        actionChains.click_and_hold(slider).perform()
        for x in track:
            self.browser.GetActionChains().move_by_offset(xoffset=x, yoffset=0).perform()
        actionChains.pause(1)
        actionChains.release().perform()
