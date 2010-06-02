'''
Created on 31/gen/2010

@author: anonymous
'''

class Singleton(object):
        _instance = None

        @classmethod
        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super(Singleton, cls).__new__(
                                   cls, *args, **kwargs)
            return cls._instance
