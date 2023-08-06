"""TODO doc"""

import os
import pkg_resources
import random
import sys
import time

import coloredlogs
import logging
import logging.handlers

from ejerico.sdk.annotations import singleton
from ejerico.sdk.config import ConfigManager

__all__ = ["LoggingManager"]

@singleton
class LoggingManager(object):

    def __init__(self):
        self._config = ConfigManager.instance()
        self._level_name = "INFO"
        self._level = logging._nameToLevel[self._level_name]

    def boot(self):
        self._level_name = self._config.get("logging_level", default="INFO")
        self._level = logging._nameToLevel[self._level_name]
        
        self.logger = logging.getLogger('ejerico')
        #syslog_handler = logging.handlers.SysLogHandler(address = '/dev/log')
        #self.logger.addHandler(syslog_handler)
        self.logger.setLevel(self._level)
        
        coloredlogs.install(level=self._level_name)

    def getLogger(self, name=None):
        return logging.getLogger(name if name is not None else "ejerico")
