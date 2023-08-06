# -*- coding: utf-8 -*-
"""
封装操作文件功能：查
"""
import os


def check_file(route):
    if '\\' != route[0]:
        return None
    filepath = os.getcwd() + route
    path = []
    for dirpath, dirnames, filenames in os.walk(filepath):
        for names in filenames:
            path.append(os.path.join(dirpath, names))
    return path
