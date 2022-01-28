from src.exceptions.SlideError import SlideError


class SlideToWrongPositionError(SlideError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return ("滑动位置错误: {}".format(repr(self.value)))