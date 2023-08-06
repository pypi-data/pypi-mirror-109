"""TODO doc"""

import inspect
import os
import pkg_resources
import random
import sys
import time
import uuid
import logging

from ejerico.sdk.annotations import singleton
from ejerico.sdk.config import ConfigManager
from ejerico.sdk.logging import LoggingManager

__all__=["StatManager","Stat"]

@singleton
class StatManager(object):
    """TODO doc"""

    def __init__(self):
        self._config = ConfigManager.instance()
        self._logger = LoggingManager.instance().getLogger()
        self._stats = {}

    def boot(self):
        #get stats/metrics url parameters from config
        pass

    def getStat(self, name=None):
        if name is None:
            name = self.__inferCallerID()

        if name not in self._stats:
            self._stats[name] = Stat(name)

        return self._stats[name]

    def releaseStat(self, name=None):
        if name is None:
            name = self.__inferCallerID()

        if name in self._stats:
            del self._stats[name]

    def __inferCallerID(self):
        try:
            caller = sys._getframe(2)
            caller_locals = caller.f_locals
            caller_ID = caller_locals["self"].ID
            return caller_ID
        except Exception as e:
            logging.info(e)

        return uuid.uuid4() 

class Stat(object):
    """TODO doc"""

    def __init__(self, ID):
        object.__init__(self)
        self.__dict__["_ID"] = ID
        self.__dict__["_data"] = {}
        
    def __getattr__(self, name):
        if name  == "_ID":
            return self.__dict__[name]
        if name  == "_data":
            return self.__dict__[name]
        
        rst = self._data[name] if name in self._data else None
        return rst
    
    def __setattr__(self, name, value):
        if name  == "_ID":
             object.__setattr__(self, name, value)
        if name  == "_data":
             object.__setattr__(self, name, value)
        else:
            self._data[name] = value

    def send(self):
        pass

    def clear(self):
        pass

    @property
    def ID(self):
        return self._ID

    