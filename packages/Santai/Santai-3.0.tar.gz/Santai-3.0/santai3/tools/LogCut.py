#coding=utf-8
__author__ = 'zoulida' #日志循环覆盖
import glob
import logging
import logging.handlers

class Logger():
    def __init__(self, logName, logLevel, logger):

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件

        handlerFile = logging.handlers.RotatingFileHandler(logName,
                                                       maxBytes=5000000,  # 每个文件最大的size 5M
                                                       backupCount=5,  # 最大备份文件数量
                                                       )


        # 再创建一个handler，用于输出到控制台
        handlerConsole = logging.StreamHandler()
        handlerConsole.setLevel(logLevel)

        # 定义handler的输出格式
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s \
        -[%(filename)s:%(lineno)d]')
        handlerFile.setFormatter(log_format)
        handlerConsole.setFormatter(log_format)

        # 给logger添加handler
        self.logger.addHandler(handlerFile)
        self.logger.addHandler(handlerConsole)

    def getlog(self):
        return self.logger

