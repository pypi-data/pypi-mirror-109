# -*- coding: utf-8 -*-
"""
功能：使用 selenium 执行 js 代码
"""


def get_script(driver, js):
    """
    * 执行 js 语法
    * 同步执行 js 语法
    :param driver:
    :param js: js 语法
    :return:
    """
    driver.execute_script(js)


def click_js_class(driver, _class):
    """
    * 使用 js 去点击元素。优势：（selenium click 点击是需要看的见的元素，但是 js 点击，可以不需要看到，只要在页面上就可以了）
    :param driver:
    :param _class: class  比如：（_class='sc-common-btn save-button'）
    :return:
    """
    get_script(driver, 'document.getElementsByClassName("{0}")[0].click();'.format(_class))


def stop_video(driver, location):
    """
    * 暂停视频播放
    （待测试，不一定可以用）
    :param driver:
    :param location: 定位
    :return:

    例子：driver.execute_script("return arguments[0].pause()", driver.find_element_by_css_selector('#liveFlashBox video'))
    """
    driver.execute_script("return arguments[0].pause()", location)
