class DataIsEmptyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return ("数据为空: {}".format(repr(self.value)))