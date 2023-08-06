# -*- coding: utf-8 -*-
"""
功能：使用 selenium 执行 js 代码
"""


def get_script(driver, js):
    driver.execute_script(js)


def click_js_class(driver, _class):
    get_script(driver, 'document.getElementsByClassName("{0}")[0].click();'.format(_class))


def stop_video(driver, location):
    driver.execute_script("return arguments[0].pause()", location)
