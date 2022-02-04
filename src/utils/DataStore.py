'''
Author: Nancycycycy
Date: 2022-01-25 13:23:05
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 15:21:10
Description: 数据存储类

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''

import csv
import importlib
import itertools
import os
from dataclasses import fields

from exceptions.DataIsEmptyError import DataIsEmptyError
from exceptions.EntityNotFoundError import EntityNotFoundError


class DataStore:

    def ReadLines(self, path):
        lines = []
        with open(path, 'r+', encoding='utf_8_sig') as f:
            csvReader = csv.DictReader(f)
            for row in csvReader:
                lines.append(row)
        return lines

    def SaveLines(self, path, headers: list, lines: list) -> None:
        with open(path, 'w+', encoding='utf_8_sig') as f:
            csvWriter = csv.DictWriter(f, fieldnames=headers)
            csvWriter.writeheader()
            csvWriter.writerows(lines)

    def SaveEntities(self, path, entityList: list):
        if (not entityList):
            raise DataIsEmptyError()
        headers = [field.name for field in fields(entityList[0])]
        rows = [
            dict((field.name, getattr(vo, field.name)) for field in fields(vo))
            for vo in entityList
        ]
        self.SaveLines(path, headers, rows)

    def ReadEntities(self, path) -> list:
        """读取文件并转换为对应Entity的列表

        Args:
            path (str): 读取文件路径

        Raises:
            DataIsEmptyError: 读取数据为空
            VONotFoundError: 未找到对应Entity
        """
        dictList: dict = self.ReadLines(path)
        if (not dictList):
            raise DataIsEmptyError()
        entityFolderPath = "./src/entity/"
        entityFolderFiles = []
        for root, dirs, files in os.walk(entityFolderPath):
            entityFolderFiles.append(files)
        entityFolderFiles = list(itertools.chain.from_iterable(entityFolderFiles))
        modules = list(
            filter(lambda name: "__" not in name and ".pyc" not in name,
                   entityFolderFiles))
        modules = [modName[:-3] for modName in modules]
        for modName in modules:
            module = importlib.import_module(f"entity.{modName}")
            tryClass = getattr(module, modName)()
            columns = set([field.name for field in fields(tryClass)])
            dictHeaders = set(dictList[0].keys())
            if (columns == dictHeaders):
                return [
                    getattr(module, modName)(**entityDict) for entityDict in dictList
                ]
        raise EntityNotFoundError(f"entity {path} not found")
