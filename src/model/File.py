'''
Author: Yaaprogrammer
Date: 2022-02-10 16:18:18
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 21:50:24

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from peewee import BooleanField, CharField, FixedCharField, IntegerField

from model.BaseModel import BaseModel


class File(BaseModel):
    fileId = IntegerField(primary_key=True, column_name="file_id")
    key = FixedCharField(column_name="key")
    passwordUnzip = CharField(column_name="password_unzip")
    hasTransferred = BooleanField(column_name="has_transferred")
    associatedPost = IntegerField(column_name="associated_post")
