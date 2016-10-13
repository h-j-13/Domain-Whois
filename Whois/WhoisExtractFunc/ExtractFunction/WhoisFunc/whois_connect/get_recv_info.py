#!/usr/bin/python
# encoding:utf-8

# 与whois服务器通信, 获得其返回数据
# @author wangkai
# @version 1.1
# 2015.12.20

import re
import socket
import sys
import time
from random import choice
from threading import Thread

import socks
import proxy_ip
import static

reload(sys)   
sys.setdefaultencoding('utf8')

# _proxy_ip = proxy_ip.ProxyIP()  # 代理IP获取
_server_ip = static.server_ip # server_ip 获取对象

ThreadStop = Thread._Thread__stop # 获取私有函数

# 取得whois服务器返回数据, 做初步多次链接处理
# @param domain 域名(punycode)
# @param whois_srv 该域名的whois服务器地址
# @return 服务器返回数据
def get_recv_info(domain, whois_srv):
    
    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = connect(domain, whois_srv, tcpCliSock)
    for i in range(5):
        if not isError(data):
            break
        data = connect(domain, whois_srv, tcpCliSock)
    tcpCliSock.close()

    return 'ERROR OTHER' if data == None else data

error_list = ['ERROR -1', 'ERROR -2', 'ERROR -3', 'ERRER OTHER', 'Queried interval is too short.']

# 判断是否错误信息
def isError(data, tcpCliSock):
    if data == None:
        return True
    for error in error_list:
        if data.find(error) != -1:
            return True
    return False
    
class TimeoutException(Exception):
    pass
    
def timelimited(timeout):
    def decorator(function):
        def decorator2(*args,**kwargs):
            class TimeLimited(Thread):
                def __init__(self,_error= None,):
                    Thread.__init__(self)
                    self._error =  _error
                     
                def run(self):
                    try:
                        self.result = function(*args,**kwargs)
                    except Exception,e:
                        self._error =e
 
                def _stop(self):
                    if self.isAlive():
                        ThreadStop(self)
 
            t = TimeLimited()
            t.setDaemon(True) # 守护线程
            t.start()
            t.join(timeout)
            
            if isinstance(t._error,TimeoutException):
                t._stop()
                # raise TimeoutException('timeout for %s' % (repr(function)))
                return 'ERROR -1' # 超时
 
            if t.isAlive():
                t._stop()
                # raise TimeoutException('timeout for %s' % (repr(function)))
                return 'ERROR -1' # 超时
 
            if t._error is None:
                return t.result
                
        return decorator2
    return decorator


# 获取whois服务器返回数据
# @param domain 域名
# @param whois_srv 该域名的whois服务器地址
# @return 服务器返回数据
@timelimited(20)
def connect(domain, whois_srv, tcpCliSock):

    global  _server_ip
    # global _proxy_ip
    # ip, port, mode = _proxy_ip.get_proxy_ip()
    
    HOST = _server_ip.get_server_ip(whois_srv) # 服务器地址,转换为IP
    if not HOST:
       HOST = whois_srv
       
    data_result = ""
    PORT = 43           # 端口
    BUFSIZ = 1024       # 每次返回数据大小
    ADDR = (HOST, PORT)
    EOF = "\r\n"
    data_send = domain + EOF
    # socks.setdefaultproxy(proxytype = socks.PROXY_TYPE_SOCKS4 if mode == 4 else socks.PROXY_TYPE_SOCKS5, addr = ip, port = port)
    # socket.socket = socks.socksocket
    try:
        tcpCliSock.connect(ADDR)
        tcpCliSock.send(data_send)
    except socket.error, e:
        if str(e).find("timed out") != -1: #连接超时
            return "ERROR -1"
        elif str(e).find("Temporary failure in name resolution") != -1:
            return "ERROR -2"
        else:
            return "ERROR OTHER"

    while True:
        try:
            data_rcv = tcpCliSock.recv(BUFSIZ)
        except socket.error, e:
            return "ERROR -3"
        if not len(data_rcv):
            return data_result  # 返回查询结果
        data_result = data_result + data_rcv  # 每次返回结果组合

if __name__ == '__main__':

    domain = 'alphacom31.com' # raw_input("domain :")
    whois_server = 'whois.crsnic.net' # raw_input("whois_server :")

    data_result = get_recv_info(domain, whois_server)
    print data_result
