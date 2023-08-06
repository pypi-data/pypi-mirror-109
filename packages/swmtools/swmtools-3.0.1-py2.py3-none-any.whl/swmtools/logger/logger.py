"""
单例日志实现
create by swm 20210616
"""
import logging
import threading
import time
from logging import handlers


class MyLogger(object):
    _instance_lock = threading.Lock()

    def start(self, *arg, **kwargs):
        """
        level
        format :%(asctime)s %(levelname)s [%(filename)s:%(lineno)d(%(funcName)s)] %(message)s
        console
        file
        when
        backCount
        """
        self.level = (kwargs["level"] if kwargs.get("level") else "debug")
        self.fmt = (
            kwargs["format"] if kwargs.get("format") else "[%(asctime)s] - %(filename)s - %(levelname)s: %(message)s")
        self.console = (kwargs["console"] if kwargs.get("console") else True)
        self.file = (kwargs["file"] if kwargs.get("file") else None)
        self.when = (kwargs["when"] if kwargs.get("when") else "D")
        self.backCount = (kwargs["backCount"] if kwargs.get("backCount") else 3)
        self.level_relations = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }
        self.logger = logging.getLogger(__name__)
        self.format = logging.Formatter(self.fmt)
        if not self.level_relations.get(self.level):
            self.level = "debug"
        self.logger.setLevel(self.level_relations[self.level])

        if self.console:
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(self.format)
            self.logger.addHandler(streamHandler)
        if self.file:
            timeHandler = handlers.TimedRotatingFileHandler(
                filename=self.file,
                when=self.when,
                backupCount=self.backCount,
                encoding="utf-8"
            )
            timeHandler.setFormatter(self.format)
            self.logger.addHandler(timeHandler)

    def __new__(cls, *args, **kwargs):
        if not hasattr(MyLogger, "_instance"):
            with MyLogger._instance_lock:
                if not hasattr(MyLogger, "_instance"):
                    MyLogger._instance = object.__new__(cls)
                    MyLogger._instance.start(*args, **kwargs)
        time.sleep(0.1)  # 防止刚实例化就写入有可能导致的数据丢失
        return MyLogger._instance

    def get_logger(self, log_level, message, *args, **kwargs):
        """ 记录并输出日志 """
        if log_level == "INFO":
            self.logger.info(message)
        elif log_level == "DEBUG":
            self.logger.debug(message)
        elif log_level == "WARNING":
            self.logger.warning(message, *args, **kwargs)
        elif log_level == "ERROR":
            self.logger.error(message, *args, **kwargs)

    def get_logging(self):
        """"""
        return self.logger

    def info(self, message):
        """ """
        self.get_logger("INFO", message)

    def debug(self, message):
        """ """
        self.get_logger("DEBUG", message)

    def warning(self, message, *args, **kwargs):
        """ """
        self.get_logger("WARNING", message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """ """
        self.get_logger("ERROR", message, *args, **kwargs)
