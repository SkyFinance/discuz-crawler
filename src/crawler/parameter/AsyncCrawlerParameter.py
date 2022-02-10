'''
Author: Yaaprogrammer
Date: 2022-02-09 16:52:28
LastEditors: Yaaprogrammer
LastEditTime: 2022-02-10 22:43:41

Copyright (c) 2022 by Yaaprogrammer, All Rights Reserved.
'''
from typing import Any, Callable, Dict, List


class AsyncCrawlerParameter:

    def __init__(self, urlList: list, cookies: dict, itemAction: Callable[[Dict, int], Any],
                 doneAction: Callable[[List[Dict]], Any], parser: type) -> None:
        self.urlList = urlList
        self.cookies = cookies
        self.itemAction = itemAction
        self.doneAction = doneAction
        self.parser = parser
