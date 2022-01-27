class StatusDetctError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return ("帖子状态检测错误: {}".format(repr(self.value)))