from time import sleep
from utils.ConfigLoader import ConfigLoader
from data_store.DataStore import DataStore
from utils.PageParser import PageParser
from utils.SyncRequest import SyncRequest
from utils.Logging import Logging
from enums.CommentResponse import CommentResponse
from exceptions.CommentIntervalLimitError import CommentIntervalLimitError
from exceptions.CommentPerHourLimitError import CommentPerHourLimitError
from exceptions.CommentPublishError import CommentPublishError
from merry import Merry

merry = Merry()
logger = Logging()

class CommentPublisher:
    def __init__(self) -> None:
        config = ConfigLoader()
        self.cookie = config.GetSiteCookie()
        self.message = config.GetCommentMessage()
        self.sleepTime = config.GetCommentSleep()
        self.taskPosts = self.NeededToComment()

    def ReadPosts(self):
        return DataStore().ReadLines("./data/Status.csv")
        
    def NeededToComment(self):
        return list(filter(lambda post:post.isAvailable == True and post.isLocked == True,self.ReadPosts()))

    def BuildCommentUrl(self,post):
        tid = post.tid
        fid = post.fid
        return f"https://live.acgyouxi.xyz/forum.php?mod=post&action=reply&tid={tid}&fid={fid}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
    
    def BuildCommentPostData(self,post):
        return {
            "message":self.message,
            "formhash":post["formhash"],
            "usesig":"",
            "subject":""
        }
    
    @merry._try
    def CommentPost(self,post):
        merry.g.post = post
        postData = self.BuildCommentPostData(post)
        url = self.BuildCommentUrl(post)
        response = SyncRequest.Post(cookies= self.cookie,url = url ,data=postData) 
        commentResult = PageParser.ParseCommentResponse(response)
        self.HandleCommentResult(commentResult,post)
        sleep(self.sleepTime)

    @merry._try
    def HandleCommentResult(self,commentResult,post):
        merry.g.post = post
        if(commentResult == CommentResponse.success):
            if(post in self.taskPosts):
                logger.Success(f"thread={post.tid} Comment Success")
                self.taskPosts.remove(post)
        elif(commentResult == CommentPerHourLimitError):
            logger.Error(f"thread={post.tid} 每小时评论数量限制")
            raise CommentPerHourLimitError
        elif(commentResult == CommentResponse.intervalLimit):
            logger.Error(f"thread={post.tid} 两次评论时间间隔限制")
            raise CommentIntervalLimitError
        else:
            logger.Error(f"thread={post.tid} 评论出现未知错误")
            raise CommentPublishError

    @merry._except(CommentPerHourLimitError)
    def WaitForAnHour(self):
        self.AddPostToTask()
        logger.Info("触发每小时发帖限制，自动等待一小时")
        sleep(60*60)

    @merry._except(Exception)
    def HandleFailedComment(self):
        self.AddPostToTask()
    
    def AddPostToTask(self):
        post = getattr(merry.g, 'post', None)
        if(post is not None):
            logger.Info(f"thread={post.tid} 帖子评论失败，加入下一次评论队列")
            self.taskPosts.append(post)

    def StartTasks(self):
        for post in self.taskPosts:
            self.CommentPost(post)
        
def main():
    commentPublisher = CommentPublisher()
    while True:
        commentPublisher.StartTasks()
        if(not commentPublisher.taskPosts):
            logger.Info(f"全部评论执行完毕")
            break


if(__name__ == "__main__"):
    main()