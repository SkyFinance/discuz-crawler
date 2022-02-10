'''
Author: Yaaprogrammer
Date: 2022-02-10 17:02:05
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 21:50:15

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from peewee import CharField, IntegerField

from model.BaseModel import BaseModel


class PostDetail(BaseModel):
    threadId = IntegerField(primary_key=True, column_name="thread_id")
    forumId = IntegerField(column_name="forum_id")
    title = CharField(column_name="title")
