from exceptions.CommentPublishError import CommentPublishError


class CommentPerHourLimitError(CommentPublishError):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return ("每小时评论数量限制 {}".format(repr(self.value)))
