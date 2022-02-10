'''
Author: Yaaprogrammer
Date: 2022-02-10 16:57:42
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 21:50:25

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from peewee import CharField, DateField, IntegerField

from model.BaseModel import BaseModel


class FileDetail(BaseModel):
    fileId = IntegerField(primary_key=True, column_name="file_id")
    name = CharField(column_name="name")
    releaseDate = DateField(column_name="release_date")
    size = CharField(column_name="size")
