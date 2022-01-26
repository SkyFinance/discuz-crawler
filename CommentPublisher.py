from loguru import logger
from DataStore.DataStore import DataStore
from ConfigLoader import ConfigLoader
import requests
from time import sleep

class CommentPublisher:
    def __init__(self) -> None:
        config = ConfigLoader()
        self.cookie = config.GetSiteCookie()
        self.message = config.GetCommentMessage()
        self.current = 0
        self.allPosts = 0
        self.commentFaildPosts = []

    def GetPosts(self):
        dataStore = DataStore()
        posts = dataStore.ReadLines("./Data/Status.csv")
        return posts
    
    def SearchPostsNeededToComment(self,posts):
        commentPosts = []
        for post in posts:
            if(post["isAvailable"] == "True" and post["isLocked"] == "True"):
                postObject = {"postId":int(post["post"]),"tid":int(post["tid"]),"fid":int(post["fid"]),"formhash":post["formhash"]}
                commentPosts.append(postObject)
        return commentPosts

    def IsSuccess(self,html:str) -> bool:
        return html.find("回复发布成功") != -1

    def CommentPost(self,post):
        tid = post["tid"]
        fid = post ["fid"]
        formhash = post["formhash"]
        postData = {
            "message":self.message,
            "formhash":formhash,
            "usesig":"",
            "subject":""
        }
        url = f"https://live.acgyouxi.xyz/forum.php?mod=post&action=reply&tid={tid}&fid={fid}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
        response = requests.post(cookies=self.cookie,url=url,data=postData)
        self.current += 1
        if(self.IsSuccess(response.text)):
            logger.info(f"fid={fid},tid={tid},result:Success ({self.current}/({self.allPosts}))")
            if(post in self.commentFaildPosts):
                self.commentFaildPosts.remove(post)
        else:
            logger.error(f"fid={fid},tid={tid},result:Failed ({self.current}/({self.allPosts}))")
            self.commentFaildPosts.append(post)

    def GetTaskPosts(self):
        if(len(self.commentFaildPosts)==0):
            posts = self.SearchPostsNeededToComment(self.GetPosts())
        else:
            posts = self.commentFaildPosts
        return posts

    def StartComment(self):
        sleepTime = ConfigLoader().GetCommentSleep()
        posts = self.GetTaskPosts()
        self.allPosts = len(posts)
        logger.info(f"a new task created,goal:{self.allPosts}")
        for post in posts:
            self.CommentPost(post)
            sleep(sleepTime)
        if(len(self.commentFaildPosts)>0):
            self.StartComment()
        
        
def main():
    commentPublisher = CommentPublisher()
    commentPublisher.StartComment()

if(__name__ == "__main__"):
    main()