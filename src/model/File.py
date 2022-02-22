'''
Author: Yaaprogrammer
Date: 2022-02-10 16:18:18
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 16:24:00

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from peewee import BooleanField, CharField, FixedCharField, IntegerField

from model.BaseModel import BaseModel


class File(BaseModel):
    key = FixedCharField(column_name="key")
    passwordUnzip = CharField(column_name="password_unzip")
    associatedPost = IntegerField(primary_key=True,
                                  column_name="associated_post")
    isAvailable = BooleanField(column_name="is_available")
