class CommentPublishError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return ("评论发布错误: {}".format(repr(self.value)))
