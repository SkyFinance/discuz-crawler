'''
Author: Yaaprogrammer
Date: 2022-02-10 20:45:14
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 20:45:15

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''


from abc import abstractmethod


class BaseWebDriverInitializer:

    @abstractmethod
    def GetWebDriver(self):
        pass
