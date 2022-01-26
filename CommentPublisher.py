from time import sleep

import requests
from loguru import logger

from ConfigLoader import ConfigLoader
from DataStore.DataStore import DataStore


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

    def FailedReason(self,html:str) -> str:
        if(html.find("抱歉，您所在的用户组每小时限制发回帖")!= -1):
            return "每小时限制发回帖限制"
        else:
            return "发帖间隔10s限制"

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
        try:
            response = requests.post(cookies=self.cookie,url=url,data=postData)
        except requests.exceptions.ConnectionError:
            logger.error(f"fid={fid},tid={tid},ConnectionError ({self.current}/{self.allPosts})")
            self.commentFaildPosts.append(post)
        except requests.exceptions.ChunkedEncodingError:
            logger.error(f"fid={fid},tid={tid},ChunkedEncodingError ({self.current}/{self.allPosts})")
            self.commentFaildPosts.append(post)
        except:
            logger.error(f"fid={fid},tid={tid},UnknownError ({self.current}/{self.allPosts})")
            self.commentFaildPosts.append(post)
        finally:
            self.current += 1
            if(response.status_code==200):
                if(self.IsSuccess(response.text)):
                    logger.info(f"fid={fid},tid={tid},result:Success ({self.current}/{self.allPosts})")
                    if(post in self.commentFaildPosts):
                        self.commentFaildPosts.remove(post)
                else:
                    logger.error(f"fid={fid},tid={tid},result:Failed,{self.FailedReason(response.text)} ({self.current}/{self.allPosts})")
                    self.commentFaildPosts.append(post)

    def GetTaskPosts(self):
        if(self.commentFaildPosts):
            return self.commentFaildPosts
        else:
            return self.SearchPostsNeededToComment(self.GetPosts())

    def StartComment(self):
        sleepTime = ConfigLoader().GetCommentSleep()
        posts = self.GetTaskPosts()
        self.allPosts = len(posts)
        logger.info(f"a new task created,goal:{self.allPosts}")
        self.current = 0
        self.commentFaildPosts = []
        for post in posts:
            self.CommentPost(post)
            sleep(sleepTime)
        logger.info(f"a task finished.")
        if(self.commentFaildPosts):
            self.StartComment()
        
        
def main():
    commentPublisher = CommentPublisher()
    commentPublisher.StartComment()

if(__name__ == "__main__"):
    main()