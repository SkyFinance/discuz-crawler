from src.exceptions.SlideError import SlideError


class SlideRobotDetectedError(SlideError):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return ("滑动未通过人机检测: {}".format(repr(self.value)))
