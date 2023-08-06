# -*- coding: utf-8 -*-
"""
二次封装 selenium 功能：
"""

import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def chrome_head(wait=1, is_psd=True, is_image=False, is_css=False, is_audio=False, is_maximize_win=False, executable_path='Chrome/Application/chromedriver.exe'):
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('log-level=3')
    prefs = {}
    if is_psd:
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
    if is_image:
        prefs = {"profile.managed_default_content_settings.images": 2}
    if is_css:
        prefs['permissions.default.stylesheet'] = 2
    if is_audio:
        option.add_argument("--mute-audio")

    option.add_experimental_option("prefs", prefs)

    try:
        driver = webdriver.Chrome(executable_path=executable_path, chrome_options=option)
    except selenium.common.exceptions.WebDriverException:
        driver = webdriver.Chrome(chrome_options=option)
    except Exception as e:
        print(e)
        input('浏览器异常，请检查。')
        exit()
    if is_maximize_win:
        driver.maximize_window()
    driver.implicitly_wait(wait)
    return driver


def debug_chrome_head(wait=1, port=9999, is_maximize_win=False, executable_path='Chrome/Application/chromedriver.exe'):
    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:{}".format(port))
    try:
        driver = webdriver.Chrome(executable_path=executable_path, chrome_options=option)
    except selenium.common.exceptions.WebDriverException:
        driver = webdriver.Chrome(chrome_options=option)
    except Exception as e:
        print(e)
        input('浏览器异常，请检查。')
        exit()
    if is_maximize_win:
        driver.maximize_window()
    driver.implicitly_wait(wait)
    return driver


def kill():
    os.system('taskkill /f /im chromedriver.exe')


def requests_cookies(driver):
    time.sleep(1)
    cookies = '; '.join(item for item in [item["name"] + "=" + item["value"] for item in driver.get_cookies()])
    return cookies


def base_location(driver, types: list, error=True, error_log=False):
    ec = 1
    location_obj = None
    while True:
        try:
            if types[0] == 'xpath':
                location_obj = driver.find_element_by_xpath(types[1])
            elif types[0] == 'css':
                location_obj = driver.find_element_by_css_selector(types[1])
            elif types[0] == 'id':
                location_obj = driver.find_element_by_id(types[1])
            elif types[0] == 'classname':
                location_obj = driver.find_element_by_class_name(types[1])
            elif types[0] == 'name':
                location_obj = driver.find_element_by_name(types[1])
            if location_obj:
                return location_obj
        except Exception as e:
            if error_log and ec:
                ec = 0
                print(e)
            if not error:
                return location_obj


def roll(driver, types: list, error_log=False):
    ec = 1
    while True:
        try:
            location_obj = base_location(driver, types=types, error_log=error_log)
            driver.execute_script("arguments[0].scrollIntoView();", location_obj)
            break
        except Exception as e:
            if error_log and ec:
                ec = 0
                print(e)


def definitely_click_a(driver, types: list, error_log=False):
    """一定会点击一次"""
    ec = 1
    while True:
        try:
            location_obj = base_location(driver, types=types, error_log=error_log)
            location_obj.click()
            break
        except Exception as e:
            if error_log and ec:
                ec = 0
                print(e)


def definitely_click_b(driver, types: list, times=1, error_log=False):
    ec = 1
    while True:
        try:
            location_obj = base_location(driver, types=types, error=False, error_log=error_log)
            location_obj.click()
            time.sleep(times)
        except Exception as e:
            if error_log and ec:
                ec = 0
                print(e)
            break


def print_cookie(path='cookies.txt'):
    with open(path) as f:
        print('使用 cookies')
        return f.read()


def start_cookie(driver, path='cookies.txt'):
    cookies = print_cookie(path)
    for cookie in eval(cookies):
        driver.add_cookie(cookie)
    # driver.get('然后使用登录后的url，不是登录的url')


def update_cookie(driver, path='cookies.txt'):
    with open(path, 'w') as f:
        f.write(str(driver.get_cookies()))
        print('更新 cookies')


def jump_iframe(driver, types: list, error_log=False):
    ec = 1
    while True:
        try:
            location_obj = base_location(driver, types=types, error_log=error_log)
            driver.switch_to.frame(location_obj)
            break
        except Exception as e:
            if error_log and ec:
                ec = 0
                print(e)


def jump_out_iframe(driver):
    driver.switch_to.default_content()


def anti_robot(driver):
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}})


def set_download_path(driver, path):
    path = path.rstrip(os.sep)
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {'behavior': 'allow', 'downloadPath': path}
    }
    driver.execute("send_command", params)
    if not os.path.exists(path):
        os.makedirs(path)
