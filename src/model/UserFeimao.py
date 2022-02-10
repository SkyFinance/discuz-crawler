'''
Author: Yaaprogrammer
Date: 2022-02-10 17:29:22
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 21:50:17

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from peewee import CharField, DateTimeField, IntegerField

from model.BaseModel import BaseModel


class UserFeimao(BaseModel):
    userId = IntegerField(primary_key=True, column_name="user_id")
    name = CharField(column_name="name")
    cookie = CharField(column_name="cookie")
    lastLogin = DateTimeField(column_name="last_login")
