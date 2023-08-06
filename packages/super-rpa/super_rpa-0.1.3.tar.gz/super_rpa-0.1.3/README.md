# SuperRPA

## 介绍
二次封装 Selenium，并且搭载各种文本、csv、xlsx、本地文件等操作。后期会不断更新新功能。谢谢使用 ~

## 安装教程

1.  pip install super-rpa

## 使用说明

1.  from super_rpa.super_pypackage import *
2.  看源码。

## 与作者互动

* **作者**：叶狼
* **Email**：yelang97@qq.com
* **pypi地址**：https://pypi.org/project/SuperRPA/
* **了解作者更多，请查看csdn博客**：https://blog.csdn.net/weixin_42038955
* **gitee地址**：https://gitee.com/xiaoye_01/super-rpa
* **您的使用，是我最大的动力，支持开源。**


## 更新日志

* **v0.0.6** (2021.05.23)：对 xlsx 表格的显示和追加修改。
* **v0.0.7** (2021.05.27)：新增了一些 selenium 二次封装的新功能。



```
from super_rpa.super_pypackage.py_selenium import py_selenium

py_selenium.chrome_head：        浏览器头
py_selenium.kill：               杀进程
py_selenium.requests_cookies：   获取selenium的cookie并且转换成requests可用的cookie
py_selenium.base_location：      一定会定位到对象
py_selenium.roll：               滑动到指定位置
py_selenium.definitely_click_a： 一定会点击一次
py_selenium.definitely_click_b： 点到该元素点不到为止
py_selenium.print_cookie：       输出 cookie
py_selenium.start_cookie：       使用 cookie
py_selenium.update_cookie：      更新 cookie
py_selenium.jump_iframe：        进入 iframe
py_selenium.jump_out_iframe：    跳出 iframe
py_selenium.anti_robot：         反反机器人
```



