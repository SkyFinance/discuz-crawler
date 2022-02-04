class VONotFoundError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return ("未找到对应VO: {}".format(repr(self.value)))
