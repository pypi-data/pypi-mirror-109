# -*- coding: utf-8 -*-


def settings(path='config.ini'):
    """
    :param path: 路径
    :return:

    使用案例：
        .py
        user = settings()
        print(user.items('setting'))  # 读取这个组名

        .ini
        # 1、里面的键不允许重复。
        # 2、可以有多个组。

        [setting]  # 组名
        键1=值1
        键2:值2
        # 上面两种编写方式都可以，输出格式都是[(键1,值1),(键2,值2)]
    """
    import configparser
    config = configparser.ConfigParser()
    try:
        config.read(path, encoding="utf-8-sig")
    except configparser.DuplicateOptionError:
        print('有数据重复了，请检查。。')
        exit()
    return config
