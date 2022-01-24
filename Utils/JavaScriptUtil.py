from base64 import b64decode
from genericpath import exists
from os import mkdir
import os.path
class JavaScriptUtil:
    """一些使用js代码的工具方法
    """
    @staticmethod
    def ScrollToBottom(browser)->None:
        """浏览器执行js代码，滚动到底部

        Args:
            browser ([webdriver]): 浏览器对象
        """
        script = "var q=document.documentElement.scrollTop=100000"
        browser.execute_script(script)
    @staticmethod
    def SaveImageFromCanvas(browser,className,imgPath) ->None:
        """浏览器执行js代码，从Canvas中保存图像

        Args:
            browser ([webdriver]): 浏览器对象
            classname ([type]): Canvas的完整类名
        """
        script = f'return document.getElementsByClassName("{className}")[0].toDataURL("image/png");'
        imgInfo = browser.execute_script(script)
        imgBase64 = imgInfo.split(',')[1]
        imgBytes = b64decode(imgBase64)
        with open(imgPath,'wb+') as f: 
            f.write(imgBytes)
    
    @staticmethod
    def SaveBackGroundImage(browser)->None:
        """从Canvas中保存缺口图

        Args:
            browser ([webdriver]): 浏览器对象
        """
        if(not exists("./Captcha/")):
            mkdir("./Captcha/")
        JavaScriptUtil.SaveImageFromCanvas(browser,"geetest_canvas_bg geetest_absolute","./Captcha/bg.png")

    @staticmethod
    def SaveFullBackGroundImage(browser)->None:
        """从Canvas中保存完整背景图

        Args:
            browser ([webdriver]): 浏览器对象
        """
        if(not exists("./Captcha/")):
            mkdir("./Captcha/")
        JavaScriptUtil.SaveImageFromCanvas(browser,"geetest_canvas_fullbg geetest_fade geetest_absolute","./Captcha/fullbg.png")