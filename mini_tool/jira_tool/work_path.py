"""
@Author  : Li Hui
@Contact : hui.4.li@nokia-sbell
"""
import os
import sys


class WorkPath:
    def directory(self):
        # return os.path.dirname(os.path.realpath(__file__))
        return os.path.dirname(os.path.realpath(sys.argv[0]))
