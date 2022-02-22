'''
Author: Yaaprogrammer
Date: 2022-02-10 16:57:42
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 19:33:21

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from peewee import CharField, DateField, IntegerField

from model.BaseModel import BaseModel


class FileDetail(BaseModel):
    associatedPost = IntegerField(primary_key=True,
                                  column_name="associated_post")
    name = CharField(column_name="name")
    releaseDate = DateField(column_name="release_date")
    size = CharField(column_name="size")

    class Meta:
        table_name = "file_detail"
