# !/usr/bin/python
# encoding:utf-8

# 获取whois服务器的IP地址
# @author 王凯
# @version 1.0
# 2015.12.24

import static
from random import choice

class ServerIP():
    def __init__(self):
        DB = static.newDB()
        DB.get_connect()
        self.whois_ip_dict = {}
        results = DB.db_select(nature = 'server_ip')
        for result in results:
            key = result[0]
            if not result[1]:
                continue
            ip_list = result[1].split(',')
            values = []
            if result[2]:
                port_available_list = list(result[2])
                for i, ip in enumerate(ip_list):
                    if port_available_list[i] == '1':
                        values.append(ip)
            self.whois_ip_dict.setdefault(key, values)
            
       DB.db_close()
    
    # 获取whois服务器的ip地址
    # @param server_addr whois服务器
    # @return ip (若查找不到,返回None)
    def get_server_ip(self, server_addr):
        result = self.whois_ip_dict.get(server_addr, [])
        return None if not result else choice(result)
        