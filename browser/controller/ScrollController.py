from browser.Browser import Browser
class ScrollControllerController:
    """浏览器滚动控制器
    """

    def __init__(self, browser:Browser) -> None:
        self.browser = browser

    def ScrollToBottom(self) -> None:
        """浏览器执行js代码，滚动到底部
        """
        script = "var q=document.documentElement.scrollTop=100000"
        self.browser.ExecuteScript(script)
