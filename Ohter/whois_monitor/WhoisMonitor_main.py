# coding:utf-8

#
# Whois检测程序
# 实现了队列的检测，程序运行情况，速度和其他内容的检测，定期发送检测结果到邮箱中。
# version: 0.1.0
# time：2016.9.8
# author：@`13
#

# !/usr/bin/python
# encoding:utf-8

import sys
import time
from send_mail import Mail
sys.stdout.flush()
#try:
#    import schedule
#except ImportError:
#    sys.exit("无schedul模块,请安装 easy_install schedule")

if __name__ == "__main__":
    M = Mail()
    M.send_mail()
    print '初始化完成...'
    while True:
        M.send_mail()
        time.sleep(3600*1)
