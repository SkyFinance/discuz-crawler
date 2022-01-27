from exceptions.CommentPublishError import CommentPublishError


class CommentIntervalLimitError(CommentPublishError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return ("两次评论间隔限制 {}".format(repr(self.value)))