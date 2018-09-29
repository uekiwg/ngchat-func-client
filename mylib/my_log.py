# coding: utf-8
"""
"""
import os
import inspect
#import warnings

def location(depth=1):
    frame = inspect.currentframe()
    for i in range(depth):
        frame = frame.f_back
    return "{0}#{1}[{2}]".format(os.path.basename(frame.f_code.co_filename), frame.f_code.co_name, frame.f_lineno)

def debug(msg):
    print(location(2) + " : " + msg)

def info(msg):
    print("\033[36m" + location(2) + " : " + msg + "\033[0m") # CYAN

def warn(msg):
    #warnings.warn(location(2) + " : " + msg)
    print("\033[33m" + location(2) + " : " + msg + "\033[0m") # YELLOW

def error(msg):
    print("\033[31m" + location(2) + " : " + msg + "\033[0m") # RED
