# /usr/bin/python
# encoding:utf8


# 获取域名whois服务器地址
# @author 王凯
# @version 1.0
# 2015.12.23

import static
from random import choice

class ServerAddr:

    def __init__(self):

        DB = static.newDB()
        DB.get_connect()
        server_addr_dict = {}
        results = DB.db_select(nature = 'whois_addr_table')
        for result in results:
            key = result[0]
            if not result[1]:
                continue
            values = result[1].split(',')
            server_addr_dict.setdefault(key, values)

        self.server_addr_dict = server_addr_dict
        DB.db_close()

    def get_server_addr(self, tld):
        return choice(self.server_addr_dict.get(tld, None))
