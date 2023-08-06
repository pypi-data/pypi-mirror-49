# encoding:utf8
'''
base python extern lib
'''
import os
from decorator import singleton


def path_comp(tpath):
    """ fmt path uri for cross-plat """
    return tpath.replace("/", os.sep)
