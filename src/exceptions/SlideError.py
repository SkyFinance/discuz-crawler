class SlideError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return ("滑动操作错误: {}".format(repr(self.value)))