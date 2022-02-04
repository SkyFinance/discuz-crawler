'''
Author: Nancycycycy
Date: 2022-01-25 13:23:05
LastEditors: Nancycycycy
LastEditTime: 2022-02-04 13:01:46
Description: 数据存储类

Copyright (c) 2022 by Nancycycycy, All Rights Reserved.
'''

import csv
import importlib
import itertools
import os
from dataclasses import fields

from exceptions.DataIsEmptyError import DataIsEmptyError
from exceptions.VONotFoundError import VONotFoundError


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

    def SaveVOs(self, path, voList: list):
        if (not voList):
            raise DataIsEmptyError()
        headers = [field.name for field in fields(voList[0])]
        rows = [
            dict((field.name, getattr(vo, field.name)) for field in fields(vo))
            for vo in voList
        ]
        self.SaveLines(path, headers, rows)

    def ReadVOs(self, path) -> list:
        """读取文件并自动转换为对应VO的列表

        Args:
            path (str): 读取文件路径

        Raises:
            DataIsEmptyError: 读取数据为空
            VONotFoundError: 未找到对应VO
        """
        dictList: dict = self.ReadLines(path)
        if (not dictList):
            raise DataIsEmptyError()
        voFolderPath = "./vo/"
        voFolderFiles = []
        for root, dirs, files in os.walk(voFolderPath):
            voFolderFiles.append(files)
        voFolderFiles = list(itertools.chain.from_iterable(voFolderFiles))
        modules = list(
            filter(lambda name: "__" not in name and ".pyc" not in name,
                   voFolderFiles))
        modules = [modName[:-3] for modName in modules]
        for modName in modules:
            module = importlib.import_module(f"vo.{modName}")
            tryClass = getattr(module, modName)()
            columns = set([field.name for field in fields(tryClass)])
            dictHeaders = set(dictList[0].keys())
            if (columns == dictHeaders):
                return [
                    getattr(module, modName)(**voDict) for voDict in dictList
                ]
        raise VONotFoundError()
