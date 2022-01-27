from merry import Merry
from aiohttp import client_exceptions
from Logging import Logging
import requests

merry = Merry()
class SyncRequest(object):

    @staticmethod
    @merry._try
    def Post(url:str,data:dict,cookies:dict) -> str:
        """同步Post方法

        Args:
            url (str): url
            data (dict): Post数据
            cookies (dict): cookies字典

        Returns:
            str: 解码后的html
        """
        response = requests.post(url=url,data=data,cookies=cookies)
        return response.text

    @staticmethod
    @merry._except(requests.exceptions.ConnectTimeout)
    def CatchConnectTimeoutError(e):
        Logging().Error('ConnectTimeoutError: ' + str(e))
        raise e

    @staticmethod
    @merry._except(requests.exceptions.ConnectionError)
    def CatchConnectionErrorError(e):
        Logging().Error('ConnectionError: ' + str(e))
        raise e

    @staticmethod
    @merry._except(requests.exceptions.ChunkedEncodingError)
    def CatchConnectionErrorError(e):
        Logging().Error('ChunkedEncodingError: ' + str(e))
        raise e

    @staticmethod
    @merry._except(Exception)
    def CatchAll(e):
        Logging().Error('UnknownError: ' + str(e))
        raise e