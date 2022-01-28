from distutils.command.config import config
from yaml import load, FullLoader


class ConfigLoader:
    @staticmethod
    def Get() -> None:
        return Config().ReadData()
            
def singleton(cls, *args, **kw):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return getinstance
 
@singleton
class Config:
    def __init__(self) -> None:
        with open('./resource/config.yml',encoding="utf-8") as f:
            self.data = load(f, Loader=FullLoader )
    def ReadData(self):
        return self.data