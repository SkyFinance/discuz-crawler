'''
Author: Yaaprogrammer
Date: 2022-01-27 18:26:33
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-04 16:58:14
Description: 控制浏览器保存图片

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from base64 import b64decode

from utils.Logging import Logging

logger = Logging()


class ImageSaveController:
    """从Canvas中保存图片
    """

    def __init__(self, browser) -> None:
        self.browser = browser

    def SaveImageFromCanvas(self, className, imgPath) -> None:
        """浏览器执行js代码，从Canvas中保存图像

        Args:
            browser ([webdriver]): 浏览器对象
            classname ([type]): Canvas的完整类名
        """
        script = f'return document.getElementsByClassName("{className}")[0].toDataURL("image/png");'
        imgInfo = self.browser.ExecuteScript(script)
        imgBase64 = imgInfo.split(',')[1]
        imgBytes = b64decode(imgBase64)
        with open(imgPath, 'wb+') as f:
            f.write(imgBytes)
