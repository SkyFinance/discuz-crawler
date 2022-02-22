'''
Author: Yaaprogrammer
Date: 2022-02-10 16:59:47
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-22 13:37:46

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from peewee import AutoField, BooleanField

from model.BaseModel import BaseModel


class FileTransferred(BaseModel):
    fileId = AutoField(column_name="file_id")
    hasTransferred = BooleanField(column_name="has_transferred")
