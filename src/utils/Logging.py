import os
import datetime
from loguru import logger

class Logging:
    __instance = None
    DATE = datetime.datetime.now().strftime('%Y-%m-%d')
    logPath = os.path.join(os.path.dirname(os.getcwd()), "logs")
    if not os.path.isdir(logPath): os.makedirs(logPath)
    logger.add('%s\%s.log' % (logPath, DATE),
               format="{time:YYYY-MM-DD HH:mm:ss}  | {level}> {elapsed}  | {message}",
               encoding='utf-8',
               retention='1 days',
               backtrace=True,
               diagnose=True,
               enqueue=True,
              ) 

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Logging, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
 
    def Info(self, msg, *args, **kwargs):
        return logger.info(msg, *args, **kwargs)
 
    def Debug(self, msg, *args, **kwargs):
        return logger.debug(msg, *args, **kwargs)
 
    def Warning(self, msg, *args, **kwargs):
        return logger.warning(msg, *args, **kwargs)
 
    def Error(self, msg, *args, **kwargs):
        return logger.error(msg, *args, **kwargs)

    def Success(self, msg, *args, **kwargs):
        return logger.success(msg, *args, **kwargs)
 
    def Exception(self, msg, *args, excInfo=True, **kwargs):
        return logger.exception(msg, *args, exc_info=excInfo, **kwargs)