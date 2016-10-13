#!/usr/bin/python
#encoding:UTF-8

"""
二级服务器返回信息检查
"""

import re
import os
import socket
import datetime


def get_recv_info(domain, whois_srv):
    """
    与whois服务器建立连接，获得whois信息
    """
    HOST = whois_srv    # 服务器地址
    data_result = ""
    PORT = 43           # 端口
    BUFSIZ = 1024       # 每次返回数据大小
    ADDR = (HOST, PORT)
    EOF = "\r\n"
    data_send = domain + EOF
    socket.setdefaulttimeout(20)  # 超时时间
    try:
        tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.send(data_send)
    except socket.error, e:
        #print e
        tcpCliSock.close()
        if e == "time out": #连接超时
            return "ERROR -1"
        elif e == "Temporary failure in name resolution":
            return "ERROR -2"

    while True:
        try:
            data_rcv = tcpCliSock.recv(BUFSIZ)
        except socket.error, e:
            #print 'Receive Failed'
            tcpCliSock.close()
            return "ERROR -3"
        if not len(data_rcv):
            tcpCliSock.close()
            # print data_result
            return data_result  # 返回查询结果
        data_result = data_result + data_rcv  # 每次返回结果组合

def data_deal(data):

    # domain_whois = {'domain': "",      #域名
    # 'flag': 0,                              #状态标记，0表示没有whois信息，1表示存在whois信息
    # 'top_whois_server': "",                 #顶级域名服务器
    # "sec_whois_server": "",                 #二级域名服务器
    # "reg_name": "",                            #注册姓名
    # "reg_phone": "",                           #注册电话
    # "reg_email": "",                            #注册email
    # "org_name": "",                            #注册公司名称
    # "creation_date": "",                       #创建时间
    # "expiration_date": "",                   #到期时间
    # "updated_date": "",                      #更新时间
    # "insert_time": "",                          #信息插入时间
    # "details": "",                                 #细节
    # }

    sign = 0
    pattern = re.compile(
         r'(Last updated Date:.*|Last Updated On:.*\
|Update Date:.*|Registrant Phone ?:.*|Registrant Name:.*\
|Registrant Organization:.*|Registrant Email:.*\
|Registrant Phone Number:.*|Updated Date:.*\
|Creation Date ?:.*|Expiration Date:.*\
|Creation date:.*|Created Date:.*|Registrant Organisation:.*\
|Registrant E-mail:.*|Update date:.*|Created On:.*\
|Expiration date:.*|Updated date:.*\
|Registrant Firstname:.*\nRegistrant Lastname:.*|Expiry Date:.*\
|Create Date:.*)')
    match = pattern.findall(data)
    match_length = len(match)
    i = 0
    sign_org = 0
    sign_update = 0
    if match:
        print match
        for i in range(match_length):
            if match[i].split(':')[0].strip() == 'Registrant Phone' or \
                match[i].split(':')[0].strip() == 'Registrant Phone Number':
                sign += 1
                print 'Here is OK_1'
            elif match[i].split(':')[0].strip() == 'Registrant Name':
                sign += 1
                print 'Here is OK_2'
            elif match[i].find('Firstname') != -1 and match[i].find('Lastname') != -1:
                sign += 1
                print 'Here is OK_2'
                reg_name = match[i].split('\n')[0].split(':')[1].strip() + ' ' + \
                    match[i].split('\n')[1].split(':')[1].strip()
                print reg_name

            elif match[i].split(':')[0].strip() == 'Registrant Email' or \
            match[i].split(':')[0].strip() == 'Registrant E-mail':
                sign += 1
                print 'Here is OK_3'
            elif match[i].split(':')[0].strip() == 'Registrant Organization' or \
                match[i].split(':')[0].strip() == 'Registrant Organisation':
                sign += 1
                sign_org = 1
                print 'Here is OK_4'
            elif match[i].split(':')[0].strip() == 'Updated Date' or \
                match[i].split(':')[0].strip() == 'Update Date' or \
                match[i].split(':')[0].strip() == 'Last updated Date' or \
                match[i].split(':')[0].strip() == 'Update date' or \
                match[i].split(':')[0].strip() == 'Last Updated On' or \
                match[i].split(':')[0].strip() == 'Updated date':
                sign += 1
                sign_update = 1
                print 'Here is OK_5'
            elif match[i].split(':')[0].strip() == 'Creation Date' or \
                match[i].split(':')[0].strip() == 'Creation date' or \
                match[i].split(':')[0].strip() == 'Created Date' or \
                match[i].split(':')[0].strip() == 'Created On' or \
                match[i].split(':')[0].strip() == 'Create Date':
                sign += 1
                print 'Here is OK_6'
            elif match[i].split(':')[0].strip() == 'Expiration Date' or \
                match[i].split(':')[0].strip() == 'Expiration date' or \
                match[i].split(':')[0].strip() == 'Expiry Date':
                sign += 1
                print 'Here is OK_7'

    if sign == 6 and sign_org == 0:
        sign += 1
    if sign == 6 and sign_update == 0:
        sign += 1

    return sign

def flag_manage(domain_whois):
    """
    状态标记的处理
    """

    if domain_whois['details'] == 'ERROR -1': #连接超时
        flag = -1
        domain_whois['details'] = ''
    elif domain_whois['details'] == 'ERROR -2': #解析失败 Temporary failure in name resolution
        flag = -2
        domain_whois['details'] = ''
    elif domain_whois['details'] == 'ERROR -3': #无法连接
        flag = -3
        domain_whois['details'] = ''
    elif domain_whois['details'] == 'ERROR OTHER': #其他错误
        flag = -4
        domain_whois['details'] = ''
    elif domain_whois['details'] == '': #没有任何返回数据
        flag = 0
    else:
        if domain_whois['reg_name'] and domain_whois['reg_phone'] and domain_whois['reg_email'] and \
            domain_whois['org_name']: # 注册者信息完整
            flag_a = 2
        elif domain_whois['reg_name'] or domain_whois['reg_phone'] or domain_whois['reg_email'] or \
            domain_whois['org_name']: # 注册者信息不完善
            flag_a = 1
        else: # 无注册者信息
            flag_a = 0

        if domain_whois['creation_date'] and domain_whois['updated_date'] and domain_whois['expiration_date']:
            # 注册日期信息完整
            flag_b = 2
        elif domain_whois['creation_date'] or domain_whois['updated_date'] or domain_whois['expiration_date']:
            # 注册日期信息不完善
            flag_b = 1
        else: # 无注册日期信息
            flag_b = 0

        flag = 100 + flag_a * 10 + flag_b

    domain_whois['flag'] = flag
    return domain_whois

if __name__ == '__main__':

    f_read = open('-3_4_error_whois_addr.txt')
    f_write = open('error_whois_addr_6.txt', 'w+')
    f_write_3 = open('-3_5_error_whois_addr.txt', 'w+')
    line = f_read.readline()
    i = 0
    while line:
        i += 1
        whois_addr = line.split(':')[0].strip().split('<<')[1].strip()
        domain = line.split(':')[1].strip()
        data = get_recv_info(domain, whois_addr)
        sign_exit = 0
        while data == 'ERROR -3' and sign_exit < 5:
            data = get_recv_info(domain, whois_addr)
            sign_exit += 1
        
        # result = flag_manage(data_deal(data))
        # sign = result['flag']

        sign = data_deal(data)
        print '==>', sign, '<==' 

        if data == 'ERROR -3':
            print i, 'ERROR -3'
            f_write_3.write(line)
        elif sign != 7:
            print i, 'FALSE'
            print line
            f_write.write(str(sign)+ ' ' + line)
        else:
            print i, 'TRUE'
            print line

        line = f_read.readline()

    f_read.close()
    f_write.close()
