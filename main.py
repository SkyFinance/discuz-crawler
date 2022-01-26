from loguru import logger
import sys
import getopt
from PostStatusDetector import PostStatusDetector
from CommentPublisher import CommentPublisher
from Banner import Banner


def main(argv):
    print(Banner().GetContent())
    try:
        opts, args = getopt.getopt(argv, "hdc")
    except getopt.GetoptError:
        print("Please type \"python main.py -h\" for help")
        sys.exit(2)
    if(len(opts) == 0):
        print("Please type \"python main.py -h\" for help")
        sys.exit()
    for opt,arg in opts:
        if opt == '-h':
            print('"python main.py -d" detect all posts and save the results to /Data/Status.csv')
            print('"python main.py -c" comment all available posts in /Data/Status.csv')
            sys.exit()
        elif(opt == "-d"):
            logger.info("Start detect threads.")
            detector = PostStatusDetector()
            detector.StartCorotinue()
        elif(opt == "-c"):
            logger.info("Start comment threads.")
            commentPublisher = CommentPublisher()
            commentPublisher.StartComment()
            

if(__name__ == "__main__"):
    main(sys.argv[1:])
