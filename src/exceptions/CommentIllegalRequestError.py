from exceptions.CommentPublishError import CommentPublishError


class CommentIllegalRequestError(CommentPublishError):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return ("非法字符 {}".format(repr(self.value)))
