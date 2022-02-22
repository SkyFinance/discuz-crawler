'''
Author: Yaaprogrammer
Date: 2022-01-26 14:21:51
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 16:03:47
Description: 入口模块

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
import getopt
import sys

from module.CommentPublisher import CommentPublisher
from module.FeiMaoDiskTransferor import FeiMaoDiskTransferor
from module.FileStatusDetector import FileStatusDetector
from module.PostStatusDetector import PostStatusDetector
from utils.Banner import Banner
from utils.Logging import Logging

logger = Logging()


def main(argv):

    print(Banner().GetContent())
    try:
        opts, args = getopt.getopt(argv, "hdcfk")
    except getopt.GetoptError:
        print("Please type \"python main.py -h\" for help")
        sys.exit(2)
    if (len(opts) == 0):
        print("Please type \"python main.py -h\" for help")
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print('"python main.py -d" detect all posts and save the results')
            print('"python main.py -c" comment all available posts')
            print('"python main.py -f" selenium transform pan')
            print('"python main.py -k" detect all disk file')
            sys.exit()
        elif (opt == "-d"):
            logger.Info("Start to detect threads.")
            detector = PostStatusDetector()
            detector.Start()
        elif (opt == "-c"):
            logger.Info("Start to comment threads.")
            commentPublisher = CommentPublisher()
            commentPublisher.StartTasks()
        elif (opt == "-f"):
            logger.Info("Start to transfer resource.")
            feiMaoDiskTransferor = FeiMaoDiskTransferor()
            feiMaoDiskTransferor.StartTasks()
        elif (opt == "-k"):
            logger.Info("Start to detect resource.")
            fileStatusDetector = FileStatusDetector()
            fileStatusDetector.StartTasks()


if (__name__ == "__main__"):
    main(sys.argv[1:])
