# !/usr/bin/python
#encoding:UTF-8

# whois信息测试

import re
import os
import socket
import datetime
import domain_status
# import proxy_ip
import socks
# _proxy_ip = proxy_ip.ProxyIP()
# 与whois服务连接获取whois信息
def get_recv_info(domain, whois_srv):

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
        print e
        tcpCliSock.close()
        if str(e).find("time out") != -1: #连接超时
            return "ERROR -1"
        elif str(e).find("Temporary failure in name resolution") != -1:
            return "ERROR -2"
        else:
            return 'ERROR other'

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
#两次匹配
def vg_manage(data, domain_whois):
    if data.find('NO OBJECT FOUND') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''
    domain_status = ''

    pattern = re.compile(r'(   Estatus del dominio:.*|   Fecha de Creacion:.*|   Registrado por:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Estatus del dominio':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Fecha de Creacion':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrado por':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip().split(' ')[0].strip()


    pattern2 = re.compile(r'(Servidor\(es\) de Nombres de Dominio([\s\S]*?)NIC-)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if line and line.find('Servidor(es) de Nombres de Dominio')==-1 and line.find('NIC')==-1:
                name_server += line.strip().strip('-').strip()
                name_server += ';'

    pattern4 = re.compile(r'(Titular([\s\S]*?)   Nombre de Dominio)')
    for match4 in pattern4.findall(data):
        pattern3 = re.compile(r'.*?\d+-\d*.*|.*?@.*\..*?')
        data2 = "".join(tuple(match4)[0])
        for match3 in pattern3.findall(data2):
            if match3.find('@')!=-1:
                for item in match3.split('\t'):
                    if item.find('@')!=-1:
                        domain_whois['reg_email'] = item.strip()
            else :
                if match3.find("(FAX)")!=-1:
                    domain_whois['reg_phone'] = match3.split('(FAX)',1)[1].strip()
                else :
                    domain_whois['reg_phone'] = match3.split('\t', 1)[0].strip()

    domain_whois['domain_whois'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
#正常
def nl_manage(domain_whois, data):
    if data.find('No Match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Created on:.*|Last Updated on:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Created on':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Last Updated on':
            domain_whois['expiration_date'] = match.split(':')[1].strip()

    pattern2 = re.compile(r'(Name Servers([\s\S]*?)Created on)')
    for match4 in pattern2.findall(data):
        for line in str(match4[0]).split("\n"):
            if line:
                if line.find("Name Servers") == -1 and line.find(
                        "Created on") == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
def zz_manage(data, domain_whois):
    if data.find('No records for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':', 1)[1].strip()
            domain_status += ';'

    pattern4 = re.compile(r'(Registrant:([\s\S]*?)Administrative Contact)')
    for match4 in pattern4.findall(data):
        print match4

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
def aa_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(	Registrant Name :.*|	Registrant Phone :.*|	Registrant E-mail:.*|	Updated Date	:.*|\
                        |	Creation Date	:.*|	Expiration Date	:.*|	Name Server.*|	Registrar :.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Phone':
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant E-mail':
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Name Server') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois
#...
def d2z_manage(data, domain_whois):
    if data.find('01-Jan-1970 EDT') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(	Registrar :.*|	Record created on.*|	Record expires on.*|  Record created on.*|	Record last updated on.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('Record created') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Record expires on') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Record last updated on') != -1:
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find('Registrar') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()


    pattern2 = re.compile(r'(Domain Name Servers in listed order:([\s\S]*?)# KOREAN)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if line and line.find('Domain Name Servers in listed order') == -1 and line.find('# KOREAN') == -1:
                name_server += line.strip()
                name_server += ';'

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
#一次匹配
def tz_manage(data, domain_whois):
    if data.find('NO OBJECT FOUND') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    name_server = ''

    pattern = re.compile(r'(changed:.*|registered:.*|expires:.*|nameserver:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'changed':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'expires':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'nameserver':
            for item in match.split(':')[1].strip().split(','):
                name_server += item
                name_server += ';'

    pattern2 = re.compile(r'(holder([\s\S]*?)admin_c)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(name:.*|phone:.*|email:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip().find('phone') != -1:
                domain_whois['reg_phone'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('name') != -1:
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('email') != -1:
                domain_whois['reg_email'] = match3.split(':')[1].strip()

    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
def general_manage(data, domain_whois):
    sign_not_exist_list = ['No match for', 'Available\nDomain', 'The queried object does not exist:', \
                           'Requested Domain cannot be found', 'The queried object does not exist: Domain name', \
                           'No Data Found', 'Domain Status: No Object Found', 'Domain not found.',
                           'no matching objects found', \
                           'No matching record.', 'No match', '\" is available for registration', '\"  not found', \
                           'This domain name has not been registered.', 'NOT FOUND', 'Status: Not Registered', \
                           'The queried object does not exists'

                           ]
    for sign_not_exist in sign_not_exist_list:
        if data.find(sign_not_exist) != -1:
            domain_whois['status'] = 'NOTEXIST'
            return domain_whois

    status = ''
    name_server = ''

    pattern = re.compile(r'(Last updated Date ?:.*|Last Updated On ?:.*\
|Update Date ?:.*|Registrant Phone ?:.*|Registrant Name ?:.*\
|Registrant Organization ?:.*|Registrant Email ?:.*\
|Registrant Phone Number ?:.*|Updated Date ?:.*\
|Creation Date ?:.*|Expiration Date ?:.*|Expires On ?:.*\
|Creation date ?:.*|Created Date ?:.*|Registrant Organisation ?:.*\
|Registrant E-mail ?:.*|Update date ?:.*|Created On ?:.*\
|Expiration date ?:.*|Updated date ?:.*|Updated On ?:.*\
|Registrant Firstname ?:.*\nRegistrant Lastname ?:.*|Expiry Date ?:.*\
|registrant-name:.*\nRegistrant Lastname ?:.*|Expiry Date ?:.*\
|Create Date ?:.*|Status:.*|Registrar:.*|Name Server:.*)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Registrant Phone' or \
                        match.split(':')[0].strip() == 'Registrant Phone Number':
            domain_whois['reg_phone'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()

        elif match.find('Firstname') != -1 and match.find('Lastname') != -1:
            reg_name = match.split('\n')[0].split(':')[1].strip() + ' ' + \
                       match.split('\n')[1].split(':')[1].strip()
            domain_whois['reg_name'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Registrant Email' or \
                        match.split(':')[0].strip() == 'Registrant E-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Registrant Organization' or \
                        match.split(':')[0].strip() == 'Registrant Organisation':
            domain_whois['org_name'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Updated Date' or \
                        match.split(':')[0].strip() == 'Update Date' or \
                        match.split(':')[0].strip() == 'Last updated Date' or \
                        match.split(':')[0].strip() == 'Update date' or \
                        match.split(':')[0].strip() == 'Last Updated On' or \
                        match.split(':')[0].strip() == 'Updated date' or \
                        match.split(':')[0].strip() == 'Updated On':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()

        elif match.split(':')[0].strip() == 'Creation Date' or \
                        match.split(':')[0].strip() == 'Creation date' or \
                        match.split(':')[0].strip() == 'Created Date' or \
                        match.split(':')[0].strip() == 'Created On' or \
                        match.split(':')[0].strip() == 'Create Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()

        elif match.split(':')[0].strip() == 'Expiration Date' or \
                        match.split(':')[0].strip() == 'Expiration date' or \
                        match.split(':')[0].strip() == 'Expiry Date' or \
                        match.split(':')[0].strip() == 'Expires On':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

        elif match.split(':')[0].strip() == 'Status':
            status += match.split(':', 1)[1].strip().split(' ')[0].strip().upper()
            status += ';'

        elif match.find('Registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

        elif match.find('Name Server:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['status'] = status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois
#Domain server
def nc_manage(data, domain_whois):

    if data.find('not found') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Created on 		.*|Expires on 		:.*|Last updated on 	:.*|Domain server.*|Registrant name 	:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('Domain server')!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.split(':')[0].strip() == 'Created on':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Expires on':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant name':
            domain_whois['reg_name'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return  domain_whois
#Registrant Organization
def nz_manage(data, domain_whois):

    if data.find('220 Available') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(query_status:.*|domain_dateregistered:.*|domain_datebilleduntil:.*|domain_datelastmodified:.*|\
registrar_name:.*|registrant_contact_name:.*|registrant_contact_phone:.*|registrant_contact_email:.*|ns_name.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'registrar_name':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'query_status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'registrant_contact_name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'domain_dateregistered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'domain_datebilleduntil':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'domain_datelastmodified':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_name':
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_phone':
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_email':
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()
        elif match.find("ns_name") != -1:
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
#Nameservers
def asia_manage(data, domain_whois):

    if data.find('NOT FOUND') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(created:.*|last modified:.*|renewal date:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'last modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'renewal date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    domain_whois['details'] = str(data)

    return domain_whois
#NS 1
#简单
def gov_manage(data, domain_whois):
    if data.find('Invalid query') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Creation Date:.*|Expiration Date:.*|Status:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    pattern2 = re.compile(r'(Owner contact([\s\S]*?)Admin contact)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Organization:.*|Name:.*|E-mail:.*|Phone:.*)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Organization':
                domain_whois['org_name'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'E-mail':
                domain_whois['reg_email'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match3.split(':', 1)[1].strip()
    pattern2 = re.compile(r'(Organisation([\s\S]*?)Domain Nameservers)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Organization:.*|Name:.*|E-mail:.*|Phone:.*)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Organization':
                domain_whois['org_name'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'E-mail':
                domain_whois['reg_email'] = match3.split(':', 1)[1].strip()
            elif match3.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match3.split(':', 1)[1].strip()

    pattern3 = re.compile(r'(Domain Nameservers([\s\S]*?)Domain registered)')
    for match3 in pattern3.findall(data):
        data3 = "".join(tuple(match3)[0])
        for line in data3.split('\n'):
            if line:
                if line.find("Domain Nameservers") == -1 and line.find("Domain registered") == -1:
                    name_server += line.strip()
                    name_server += ';'
    pattern3 = re.compile(r'(Domain Nameservers([\s\S]*?)Your selected domain name)')
    for match3 in pattern3.findall(data):
        data3 = "".join(tuple(match3)[0])
        for line in data3.split('\n'):
            if line:
                if line.find("Domain Nameservers") == -1 and line.find("Your selected domain name") == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois
def as_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Registrant:.*\n.*|Registrar:.*\n.*|Registration status:\n.*|Registered on.*|Registry fee due on.*)')
    for match in pattern3.findall(data):
        if match.find("Registered on") != -1:
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.find('Registry fee due') != -1:
            domain_whois['expiration_date'] = match.split('on',1)[1].strip()
        elif match.split('\n',1)[0].find('Registrant') != -1:
            domain_whois['reg_name'] = match.split('\n',1)[1].strip()
        elif match.split('\n',1)[0].find('Registrar') != -1:
            domain_whois['sponsoring_registrar'] = match.split('\n',1)[1].strip()
        elif match.split('\n',1)[0].find('Registration status') != -1:
            domain_status += match.split('\n',1)[1].strip()
            domain_status += ';'

    pattern2 = re.compile(r'(Name servers([\s\S]*?)WHOIS lookup made)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find("Name servers") == -1 and line.find("WHOIS lookup made") == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
def be_manage(data, domain_whois):
    if data.find('Not Registered') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*|Created:.*|Modified:.*|Expires:.*|Registrar Name:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expires':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrar Name':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

    pattern2 = re.compile(r'(Registrant([\s\S]*?)Admin Contact)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(International Name:.*|International Organisation:.*|Email Address:.*|Phone Number:.*)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip().find('International Name') != -1:
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('International Organisation') != -1:
                domain_whois['org_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Email Address':
                domain_whois['reg_email'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Phone Number':
                domain_whois['reg_phone'] = match3.split(':')[1].strip()


    pattern3 = re.compile(r'(Name Servers:([\s\S]*)Registrar Information)')
    for match2 in pattern3.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find("Name Servers") == -1 and line.find("Registrar Information") == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
def bo_manage(data, domain_whois):
    if data.find('solo acepta') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern3 = re.compile(r'(Registrant:\n.*|Registrar:\n.*|Registration status:\n.*|Registered on.*|Registry fee due on.*)')
    for match in pattern3.findall(data):
        if match.split(':')[0].strip() == 'Fecha de registro':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Fecha de vencimiento':
            domain_whois['expiration_date']  = match.split(':')[1].strip()

    pattern2 = re.compile(r'(TITULAR([\s\S]*?)CONTACTO ADMINISTRATIVO)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2))
        pattern = re.compile(r'(Organizacion:.*|Nombre:.*|Email:.*|Telefono.*)')
        for match3 in pattern.findall(data2):
            if match3.split(':')[0].strip() == 'Organizacion':
                domain_whois['org_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Nombre':
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip() == 'Telefono':
                domain_whois['reg_phone'] = match3.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
def fr_manage(data, domain_whois):
    if data.find('AVAILABLE') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern2 = re.compile(r'(Registrant([\s\S]*?)Technical)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Name:.*|Phone:.*|Email:.*)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip().find('Name') != -1:
                domain_whois['reg_name'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('Phone') != -1:
                domain_whois['reg_phone'] = match3.split(':')[1].strip()
            elif match3.split(':')[0].strip().find('Email') != -1:
                domain_whois['reg_email'] = match3.split(':')[1].strip()

    pattern2 = re.compile(r'(Registrar([\s\S]*?)Name servers)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Name:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip().find('Name') != -1:
                domain_whois['sponsoring_registrar'] = match3.split(':')[1].strip()

    pattern2 = re.compile(r'(Name servers([\s\S]*?)Please visit)')
    for match2 in pattern2.findall(data):
        data2 = "".join(tuple(match2)[0])
        for line in data2.split('\n'):
            if line:
                if line.find('Name servers') == -1 and line.find('Please visit') == -1:
                    name_server += line.strip()
                    name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
def cf_manage(data, domain_whois):
    if data.find('No match') != -1:
        domain_whois['status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrant.*|Name Server.*|登録年月日.*|有効期限.*|\
|状態.*|Name.*|Email.*|電話番号.*|)')
    for match in pattern.findall(data):
        if match.find("状態") != -1:
            domain_status += match.split(']')[1].strip()
            domain_status += ';'
        elif match.find("Registrant") != -1:
            domain_whois['reg_name'] = match.split(']')[1].strip()
        elif match.find("登録年月日") != -1:
            domain_whois['creation_date'] = match.split(']')[1].strip()
        elif match.find("有効期限") != -1:
            domain_whois['expiration_date'] = match.split(']')[1].strip()
        elif match.find("Email") != -1:
            domain_whois['reg_email'] = match.split(']')[1].strip()
        elif match.find("電話番号") != -1:
            domain_whois['reg_phone'] = match.split(']')[1].strip()
        elif match.find("Name") != -1 and match.find("Name Server") == -1:
            domain_whois['org_name'] = match.split(']')[1].strip()
        elif match.find("Name Server") != -1:
            name_server += match.split(']')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois
if __name__ == '__main__':

    domain = 'ol22x.com.ec'
    whois_server = 'whois.nic.ec'

    domain_whois = {"domain": "",             # 域名
        "flag": 0,                            # 状态标记
        "status": "",                         # 域名状态
        "sponsoring_registrar": "",           # 注册商
        "top_whois_server": "",               # 顶级域名服务器
        "sec_whois_server": "",               # 二级域名服务器
        "reg_name": "",                       # 注册姓名
        "reg_phone": "",                      # 注册电话
        "reg_email": "",                      # 注册email
        "org_name": "",                       # 注册公司名称
        "creation_date": "",                  # 创建时间
        "expiration_date": "",                # 到期时间
        "updated_date": "",                   # 更新时间
        "insert_time": "",                    # 信息插入时间
        "details": "",                        # 细节
        "name_server": "",                    # 域名服务器
        "hash_value": 0,                      # 哈希值
    }

    domain_whois['domain'] = domain
    domain_whois['top_whois_server'] = whois_server

    data = get_recv_info(domain, whois_server)


    print '-------------------data---------------------'
    print data

    if not data:
        exit()

    print "---------------domain_whois-----------------"
    #general_manage
    result = be_manage(data, domain_whois)
    #result = general_manage(data, domain_whois)
    result['insert_time'] = str(datetime.datetime.now())
    result = flag_manage(result)
    result['status'] = domain_status.get_status_value(domain_whois['status'], domain_whois['domain'])
    result['hash_value'] = hash(domain_whois['details'])

    print "domain:                      ", result['domain']
    print "status:                      ", result['status']
    print "flag:                        ", result['flag']
    print "sponsoring_registrar:        ", result['sponsoring_registrar']
    print "top_whois_server:            ", result['top_whois_server']
    print "sec_whois_server:            ", result['sec_whois_server']
    print "reg_name:                    ", result['reg_name']
    print "reg_phone:                   ", result['reg_phone']
    print "reg_email:                   ", result['reg_email']
    print "org_name:                    ", result['org_name']
    print "updated_date:                ", result['updated_date']
    print "creation_date:               ", result['creation_date']
    print "expiration_date:             ", result['expiration_date']
    print "name_server:                 ", result['name_server']
    print "hash_value:                  ", result['hash_value']
    # print "details", result['details']

    print "--------------------------------------------"



