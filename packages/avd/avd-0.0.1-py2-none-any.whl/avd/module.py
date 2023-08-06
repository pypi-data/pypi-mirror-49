# encoding: utf-8

from abc import ABCMeta, abstractmethod


class BaseModule(object):
    
    __metaclass__ = ABCMeta

    def __init__(self, option):
        self.option = option
        self.result = {'status': 0, 'data': dict()}

    @abstractmethod
    def run(self):
        pass

    @property
    def name(self):
        return self.__class__.__name__