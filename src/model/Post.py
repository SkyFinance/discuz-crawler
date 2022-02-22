'''
Author: Yaaprogrammer
Date: 2022-02-10 16:59:47
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 13:39:08

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from peewee import AutoField, BooleanField

from model.BaseModel import BaseModel


class Post(BaseModel):
    threadId = AutoField(column_name="thread_id")
    isAvailable = BooleanField(column_name="is_available")
    isLocked = BooleanField(column_name="is_locked")
    hasResource = BooleanField(column_name="has_resource")
