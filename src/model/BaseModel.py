'''
Author: Yaaprogrammer
Date: 2022-02-10 16:14:54
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 22:24:53

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from peewee import Model, MySQLDatabase
from utils.Configuration import Configuration

name = Configuration.GetProperty("database.mysql.db_name")
host = Configuration.GetProperty("database.mysql.host")
port = Configuration.GetProperty("database.mysql.port")
user = Configuration.GetProperty("database.mysql.user")
password = Configuration.GetProperty("database.mysql.password")
print(name, host, port, user, password)
connection = MySQLDatabase(
    database=name, host=host, port=port, user=user, password=password
)


class BaseModel(Model):

    class Meta:
        database = connection
