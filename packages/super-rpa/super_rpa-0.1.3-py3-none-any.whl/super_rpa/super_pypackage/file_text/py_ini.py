# -*- coding: utf-8 -*-


def settings(path='config.ini'):
    import configparser
    config = configparser.ConfigParser()
    try:
        config.read(path, encoding="utf-8-sig")
    except configparser.DuplicateOptionError:
        print('有数据重复了，请检查。。')
        exit()
    return config
