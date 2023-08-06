# -*- coding: utf-8 -*-
"""
自动化操作键盘
"""

import pyperclip


def py_paste():
    return pyperclip.paste()


def py_copy(text):
    pyperclip.copy(text)  # 复制
    return py_paste()


