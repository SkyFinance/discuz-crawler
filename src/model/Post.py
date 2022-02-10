'''
Author: Yaaprogrammer
Date: 2022-02-10 16:59:47
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 21:49:58

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from peewee import BooleanField, IntegerField

from model.BaseModel import BaseModel


class Post(BaseModel):
    threadId = IntegerField(primary_key=True, column_name="thread_id")
    isAvailable = BooleanField(column_name="is_available")
    isLocked = BooleanField(column_name="is_locked")
